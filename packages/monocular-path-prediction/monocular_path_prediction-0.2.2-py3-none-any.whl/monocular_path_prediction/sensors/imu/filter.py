"""IMU device class compatible with resilient SerialDevice."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from loguru import logger
from py_imu.fusion.madgwick import Madgwick
from py_imu.fusion.quaternion import Quaternion, Vector3D

from monocular_path_prediction.config.definitions import IMUFilterConfig
from monocular_path_prediction.sensors.imu.data_classes import (
    GyroBias,
    IMUData,
    IMUDataFile,
)


class BaseIMUFilter(ABC):
    """Abstract base class for IMU filters."""

    def __init__(self, config: IMUFilterConfig | None = None) -> None:
        """Initialize the base IMU filter.

        :param config: filter configuration.
        """
        if config is None:
            config = IMUFilterConfig()
        self.config = config
        self._previous_timestamp: float | None = None
        self._gyro_bias: GyroBias = GyroBias.load()

    @abstractmethod
    def step(self, imu_data: IMUData) -> Quaternion:
        """Process one IMU data sample and update the orientation estimate.

        :param imu_data: IMUData sample with timestamp, accel, gyro, (optional mag).
        :return: Updated orientation as a Quaternion.
        """
        ...


class MadgwickFilter(BaseIMUFilter):
    """Madgwick IMU filter implementation."""

    def __init__(self, config: IMUFilterConfig | None = None) -> None:
        super().__init__(config)
        self._filter = Madgwick(
            frequency=1.0 / self.config.delta_time_sec, gain=self.config.gain
        )

    def step(self, imu_data: IMUData) -> Quaternion:
        """Step the Madgwick IMU filter."""
        if self._previous_timestamp is None:
            dt = self.config.delta_time_sec
            logger.debug(f"No previous timestamp; using default dt={dt:.4f}s.")
        else:
            dt = imu_data.timestamp - self._previous_timestamp

            if abs(dt) > 10 * self.config.delta_time_sec:
                logger.warning(
                    f"Large timestamp: "
                    f"dt={dt:.4f}s. "
                    f"Clipping to default dt={self.config.delta_time_sec:.4f}s."
                )
                dt = np.clip(dt, 0, self.config.delta_time_sec)
            dt = max(0.0, dt)

        self._previous_timestamp = imu_data.timestamp

        accel = Vector3D(
            x=imu_data.accel.x.item(),
            y=imu_data.accel.y.item(),
            z=imu_data.accel.z.item(),
        )
        gyro = Vector3D(
            x=imu_data.gyro.x.item() - self._gyro_bias.x,
            y=imu_data.gyro.y.item() - self._gyro_bias.y,
            z=imu_data.gyro.z.item() - self._gyro_bias.z,
        )
        self._filter.update(gyr=gyro, acc=accel, dt=dt)
        quat = self._filter.q  # x, y, z, w

        if quat is not None:
            logger.debug(
                f"IMU: dt={dt:.4f}s, "
                f"quat(xyzw)={quat.x:.3f}, "
                f"{quat.y:.3f}, "
                f"{quat.z:.3f}, "
                f"{quat.w:.3f}"
            )
            return quat

        else:
            logger.debug(f"IMU: dt={dt:.4f}s, quat(xyzw)=None")
            raise ValueError("IMU orientation is None.")


def process_imu_data_frame_with_filter(
    imu_data_frame: IMUDataFile,
) -> list[list[Quaternion]]:
    """Process IMU data frame with filter."""
    num_imus = len(imu_data_frame.accels)
    filters = [MadgwickFilter() for _ in range(num_imus)]
    quaternions: list[list[Quaternion]] = [[] for _ in range(num_imus)]
    for imu_data in imu_data_frame:
        for idx, data in enumerate(imu_data):
            quat = filters[idx].step(data)
            quaternions[idx].append(quat)

    if len(quaternions) == 0:
        msg = "No IMU data frame filtered."
        logger.debug(msg)
        raise ValueError(msg)

    return quaternions
