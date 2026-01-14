"""IMU device class compatible with resilient SerialDevice."""

from __future__ import annotations

import ast
import re
import threading
import time

import numpy as np
from loguru import logger
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation as Rot

from monocular_path_prediction.config.definitions import IMUReaderConfig
from monocular_path_prediction.sensors.device.serial_device import (
    SerialConfig,
    SerialDevice,
)
from monocular_path_prediction.sensors.imu.data_classes import IMUData, Vector3D
from monocular_path_prediction.sensors.imu.filter import BaseIMUFilter, MadgwickFilter
from monocular_path_prediction.sensors.imu.writer import IMUFileWriter
from monocular_path_prediction.utils import nanoseconds_to_seconds


class IMUDevice(SerialDevice):
    """Parse IMU lines from a SerialDevice and maintain latest pose."""

    def __init__(self, config: SerialConfig | None = None, record_data: bool = False):
        """Initialize IMU device and start parsing thread.

        The underlying SerialDevice opens and starts its background reader.
        We start an additional parser thread that consumes the newest line and
        updates the IMU pose via a Madgwick filter.
        """
        super().__init__(config=config)
        self.imu_config = IMUReaderConfig()

        self.data_recorder: IMUFileWriter | None = (
            IMUFileWriter() if record_data else None
        )

        self.filter: list[BaseIMUFilter] = [MadgwickFilter(), MadgwickFilter()]

        self._latest_data: list[IMUData] | None = None
        self.pose: list[NDArray] | None = None
        self._previous_timestamp: float | None = None

        self._parser_thread = threading.Thread(
            target=self._parser_loop, name="IMUParser", daemon=True
        )
        self._parser_thread.start()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def __call__(self) -> tuple[list[IMUData] | None, list[NDArray] | None]:
        """Return the latest parsed IMU data and pose (non-blocking)."""
        with self._lock:
            return self._latest_data, self.pose

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #
    def _parser_loop(self) -> None:
        """Continuously parse the newest serial line and update pose."""
        logger.info("IMU parser thread started.")
        last_line: str | None = None

        while self._state.running:
            try:
                # Get most recent line from SerialDevice (non-blocking)
                line = self.latest_line()
                if not line or line == last_line:
                    time.sleep(self.config.loop_delay)
                    continue
                last_line = line
                imu_data = self._parse_imu_line(line)
                if imu_data is None:
                    continue

                # Update filter + pose
                self._update_pose(imu_data)

            except Exception as err:
                # Keep running; SerialDevice will attempt reconnects underneath
                logger.warning(f"IMU parser error: {err}")
                time.sleep(1.0)

        logger.debug("IMU parser thread exiting.")

    def _update_pose(self, imu_data: list[IMUData]) -> None:
        """Update pose using the Madgwick filter with robust dt."""
        pose = []
        latest_data = []
        for idx, data in enumerate(imu_data):
            quat = self.filter[idx].step(imu_data=data)  # x, y, z, w
            rot_matrix = Rot.from_quat(
                quat=[quat.x, quat.y, quat.z, quat.w], scalar_first=False
            ).as_matrix()
            latest_data.append(data)
            pose.append(rot_matrix)

        with self._lock:
            self._latest_data = latest_data
            self.pose = pose

        if self.data_recorder is not None:
            self.data_recorder.append_imu_data(data=imu_data)

    def _parse_imu_line(self, line: str) -> list[IMUData] | None:
        """Parse a line emitted by the IMU firmware.

        Expected format is defined by ImuConfig.time_pattern and meas_pattern.
        Example (conceptual):
            "t=123.456 <[(ax,ay,az),(gx,gy,gz),(mx,my,mz)]>"
        """
        try:
            time_match = re.search(self.imu_config.time_pattern, line)
            meas_match = re.search(self.imu_config.meas_pattern, line)
            if not time_match or not meas_match:
                logger.debug(f"IMU line did not match patterns: {line}")
                return None

            timestamp_ns = float(time_match.group(1))
            timestamp_sec = nanoseconds_to_seconds(timestamp_ns)

            # measurements are expected to be a Python-literal list/tuple string
            measurements = ast.literal_eval(meas_match.group(1))
            logger.trace(f"IMU line parsed measurements: {measurements}")
            if not measurements or not isinstance(measurements[0], tuple):
                logger.warning(f"Unexpected IMU measurement structure: {line}")
                return None

            imu_data = []
            for meas in measurements:
                if len(meas) == 2:
                    accel_tuple, gyro_tuple = meas
                    mag_tuple = (np.nan, np.nan, np.nan)
                else:
                    accel_tuple, gyro_tuple, mag_tuple = meas

                data = IMUData(
                    timestamp=timestamp_sec,
                    accel=Vector3D.from_tuple(accel_tuple),
                    gyro=Vector3D.from_tuple(gyro_tuple),
                    mag=Vector3D.from_tuple(mag_tuple),
                )

                self._check_for_clipping(imu_data=data)
                imu_data.append(data)

            return imu_data

        except Exception as err:
            logger.debug(f"Failed to parse IMU line: {err} | line='{line}'")
            return None

    def _check_for_clipping(self, imu_data: IMUData) -> None:
        """Warn when any axis exceeds the configured max value."""
        signals = [imu_data.accel, imu_data.gyro]
        max_values = [self.imu_config.accel_range_gs, self.imu_config.gyro_range_rps]
        for signal, max_value in zip(signals, max_values, strict=False):
            for v in (signal.x, signal.y, signal.z):
                if abs(v) > max_value:
                    logger.warning(f"Value {v} exceeded allowed range {max_value}.")

    def wait_for_data(self) -> tuple[list[IMUData], list[NDArray]]:
        """Block until valid IMU data and pose are available."""
        logger.trace("Waiting for IMU data...")
        imu_data, pose = None, None
        start_time = time.time()
        wait_time = self.imu_config.wait_time_sec
        while imu_data is None or pose is None:
            imu_data, pose = self.__call__()
            dt = time.time() - start_time
            if dt > wait_time:
                msg = f"Waited for IMU data for {wait_time:.2f} sec. Exiting."
                logger.error(msg)
                self.close()
                raise OSError(msg)

        logger.debug(f"IMU data: {imu_data}")
        return imu_data, pose
