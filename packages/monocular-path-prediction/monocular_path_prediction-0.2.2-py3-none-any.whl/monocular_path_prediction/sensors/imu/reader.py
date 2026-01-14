"""IMU data reading."""

from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from numpy.typing import NDArray

from monocular_path_prediction.config.definitions import IMUDataFileColumns
from monocular_path_prediction.sensors.imu.data_classes import IMUDataFile, Vector3D


def format_line(x: str) -> float:
    """Format a line from IMU data.

    :param x: a line from IMU data.
    :return: the formatted line.
    """
    if isinstance(x, str):
        x = x.strip("[]")
    return float(x)


def load_imu_data(filepath: Path) -> IMUDataFile:
    """Load IMU data from CSV file.

    :param filepath: path to CSV file.
    :return: IMU data.
    """
    logger.debug(f"Loading IMU data from '{filepath}'.")
    columns: list[str] = [col.value for col in IMUDataFileColumns]
    data_frame = pd.read_csv(
        filepath_or_buffer=str(filepath),
        usecols=columns,  # type: ignore[call-arg]
    ).map(format_line)

    time = data_frame[IMUDataFileColumns.TIMESTAMP.value].to_numpy()

    num_imus = find_num_imus(time=time)

    gyros, accels, mags = [], [], []

    for imu_idx in range(num_imus):
        gyro = Vector3D(
            data_frame[IMUDataFileColumns.GYRO_X.value].to_numpy()[imu_idx::num_imus],
            data_frame[IMUDataFileColumns.GYRO_Y.value].to_numpy()[imu_idx::num_imus],
            data_frame[IMUDataFileColumns.GYRO_Z.value].to_numpy()[imu_idx::num_imus],
        )
        gyros.append(gyro)

        accel = Vector3D(
            data_frame[IMUDataFileColumns.ACCEL_X.value].to_numpy()[imu_idx::num_imus],
            data_frame[IMUDataFileColumns.ACCEL_Y.value].to_numpy()[imu_idx::num_imus],
            data_frame[IMUDataFileColumns.ACCEL_Z.value].to_numpy()[imu_idx::num_imus],
        )
        accels.append(accel)

        mag = Vector3D(
            x=data_frame[IMUDataFileColumns.MAG_X.value].to_numpy()[imu_idx::num_imus],
            y=data_frame[IMUDataFileColumns.MAG_Y.value].to_numpy()[imu_idx::num_imus],
            z=data_frame[IMUDataFileColumns.MAG_Z.value].to_numpy()[imu_idx::num_imus],
        )
        mags.append(mag)
    return IMUDataFile(time=time[::num_imus], gyros=gyros, accels=accels, mags=mags)


def find_num_imus(time: NDArray) -> int:
    """Find number of IMU data in the recorded file.

    :param time: Timestamps array in seconds.
    :return: Number of IMU data.
    """
    num_imus = 1
    for diff in np.diff(time):
        if diff == 0.0:
            num_imus += 1
        else:
            break

    return num_imus
