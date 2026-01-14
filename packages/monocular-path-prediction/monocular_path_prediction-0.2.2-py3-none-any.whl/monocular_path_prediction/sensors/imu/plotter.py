"""IMU data plotter."""

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from matplotlib.axes import Axes
from numpy.typing import NDArray
from py_imu.fusion.quaternion import Quaternion
from scipy.spatial.transform import Rotation as Rot

from monocular_path_prediction.config.definitions import (
    DEFAULT_LOG_LEVEL,
    FigureSettings,
    IMUUnits,
)
from monocular_path_prediction.sensors.imu.data_classes import IMUDataFile
from monocular_path_prediction.sensors.imu.filter import (
    process_imu_data_frame_with_filter,
)
from monocular_path_prediction.sensors.imu.reader import load_imu_data


class IMUPlotter:  # pragma: no cover
    """Plot IMU data."""

    def __init__(
        self,
        imu_data_frame: IMUDataFile,
        quaternions: list[list[Quaternion]] | None = None,
    ) -> None:
        self.data = imu_data_frame
        self.quaternions = quaternions
        self.fig, self.axes = self._create_figs()
        self._plot_data()
        self._show()

    def _create_figs(self):
        if self.quaternions is None:
            num_rows = 3
        else:
            num_rows = 4
        fig, axes = plt.subplots(
            nrows=num_rows, ncols=1, figsize=FigureSettings.size, sharex=True
        )
        return fig, axes

    @staticmethod
    def _show():
        try:
            plt.show()
        except KeyboardInterrupt:
            plt.close()

    def _plot_data(self) -> None:
        num_imus = len(self.data.accels)
        for imu_idx in range(num_imus):
            self.data.accels[imu_idx].plot(
                ax=self.axes[0],
                time=self.data.time,
                y_label=f"Acceleration ({IMUUnits.ACCEL.value})",
            )
            self.data.gyros[imu_idx].plot(
                ax=self.axes[1],
                time=self.data.time,
                y_label=f"Angular Rate ({IMUUnits.GYRO.value})",
            )
            self.data.mags[imu_idx].plot(
                ax=self.axes[2],
                time=self.data.time,
                y_label=f"Magnetic Field ({IMUUnits.MAG.value})",
            )
        if self.quaternions is not None:
            for quat in self.quaternions:
                plot_quaternions(time=self.data.time, quaternions=quat, ax=self.axes[3])
        self.axes[-1].set_xlabel("Time (s)")
        plt.suptitle("IMU Data")
        plt.tight_layout()

    @staticmethod
    def _extract_units_from_column_name(column_name: str) -> str:
        """Extract the first substring inside parentheses."""
        match = re.search(r"\(([^)]*)\)", column_name)
        return match.group(1) if match else ""


def plot_imu_data(
    imu_data_frame: IMUDataFile, quaternions: list[list[Quaternion]] | None = None
) -> None:
    """Plot IMU data."""
    IMUPlotter(imu_data_frame=imu_data_frame, quaternions=quaternions)


def plot_quaternions(ax: Axes, time: NDArray, quaternions: list[Quaternion]) -> None:
    """Plot quaternions."""
    if quaternions is None:
        logger.warning("No quaternions provided.")
        return
    ax.scatter(time, [q.x for q in quaternions], label="x", color="r", s=1)
    ax.scatter(time, [q.y for q in quaternions], label="y", color="g", s=1)
    ax.scatter(time, [q.z for q in quaternions], label="z", color="b", s=1)
    ax.scatter(time, [q.w for q in quaternions], label="w", color="m", s=1)

    ax.set_ylabel("Quaternion")
    ax.legend()
    ax.grid(True)


def rotation_matrix_from_euler(angles: list[float]) -> np.ndarray:
    """Create a 3x3 rotation matrix from roll, pitch, yaw (in radians).

    :param angles: Rotation about the x, y, z-axis [rad].
    :return: 3x3 rotation matrix (numpy array).
    """
    rot = Rot.from_euler("xyz", angles, degrees=False)
    rot_mat = rot.as_matrix()
    logger.debug(f"Rotation matrix: {rot_mat}")
    return rot_mat


if __name__ == "__main__":  # pragma: no cover
    """Test the IMU device."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", "-f", type=Path, required=True)
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stderr, level=DEFAULT_LOG_LEVEL)

    imu_data_frame = load_imu_data(filepath=args.filepath)

    quaternions = process_imu_data_frame_with_filter(imu_data_frame=imu_data_frame)
    plot_imu_data(imu_data_frame=imu_data_frame, quaternions=quaternions)
