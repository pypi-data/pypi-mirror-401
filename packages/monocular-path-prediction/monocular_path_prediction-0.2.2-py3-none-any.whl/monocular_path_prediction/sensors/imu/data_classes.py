"""IMU data classes."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from loguru import logger
from matplotlib.axes import Axes
from numpy.typing import NDArray

from monocular_path_prediction.config.definitions import (
    GYRO_CALIBRATION_FILEPATH,
    FigureSettings,
)


@dataclass
class Vector3D:
    """3D vector data."""

    x: NDArray
    y: NDArray
    z: NDArray

    @classmethod
    def from_tuple(cls, values: tuple[float, float, float]) -> "Vector3D":
        """Create from a tuple of 3 floats.

        :param values: a tuple of 3 floats
        :return: a Vector3D
        """
        if len(values) != 3:
            raise ValueError(f"Expected 3 values, got {len(values)}")
        return Vector3D(
            x=np.array([values[0]]), y=np.array([values[1]]), z=np.array([values[2]])
        )

    def as_array(self) -> NDArray:
        """Return a numpy array representing the 3D vector.

        :return: A numpy array representing the 3D vector.
        """
        return np.array([self.x, self.y, self.z])

    def rotate(self, rotation_matrix: NDArray) -> "Vector3D":
        """Rotate the vector around the given rotation matrix.

        :param rotation_matrix: The rotation matrix to rotate.
        :return: The rotated vector.
        """
        new_vec = rotation_matrix @ self.as_array()
        return Vector3D(new_vec[0], new_vec[1], new_vec[2])

    def plot(self, ax: Axes, time: NDArray, y_label: str) -> Axes:
        """Plot 3D vector.

        :param ax: The axis to plot.
        :param time: The time to plot.
        :param y_label: The label for the plot.
        """
        alpha = FigureSettings.alpha
        ax.plot(time, self.x, label="x", color="r", alpha=alpha)
        ax.plot(time, self.y, label="y", color="g", alpha=alpha)
        ax.plot(time, self.z, label="z", color="b", alpha=alpha)
        ax.set_ylabel(y_label)
        ax.legend(loc="upper right")
        ax.grid(True)
        return ax


@dataclass
class IMUKey:
    """Class for configuring a serial device."""

    acc = "ACC"
    gyr = "GYRO"
    mag = "MAG"


@dataclass
class IMUData:
    """Represent parsed IMU data."""

    timestamp: float
    accel: Vector3D
    gyro: Vector3D
    mag: Vector3D | None = None


@dataclass
class IMUDataFile:
    """IMU data reading with Pandas."""

    time: np.ndarray
    gyros: list[Vector3D]
    accels: list[Vector3D]
    mags: list[Vector3D]

    def __iter__(self):
        """Iterate row-by-row, yielding IMUData instances."""
        n = len(self.time)
        num_imus = len(self.accels)
        for i in range(n):
            imu_data = []
            for idx in range(num_imus):
                data = IMUData(
                    timestamp=float(self.time[i]),
                    gyro=Vector3D(
                        x=self.gyros[idx].x[i],
                        y=self.gyros[idx].y[i],
                        z=self.gyros[idx].z[i],
                    ),
                    accel=Vector3D(
                        x=self.accels[idx].x[i],
                        y=self.accels[idx].y[i],
                        z=self.accels[idx].z[i],
                    ),
                    mag=Vector3D(
                        x=self.mags[idx].x[i],
                        y=self.mags[idx].y[i],
                        z=self.mags[idx].z[i],
                    ),
                )
                imu_data.append(data)
            yield imu_data


@dataclass
class GyroBias:
    """Store and manage gyroscope calibration values (bias offsets)."""

    x: float
    y: float
    z: float

    def save(self) -> None:
        """Save calibration values to a .npz file."""
        path: Path = GYRO_CALIBRATION_FILEPATH
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        np.savez(path, x=self.x, y=self.y, z=self.z)
        logger.info(f"Saving calibration values to '{path}'.")

    @classmethod
    def load(cls) -> "GyroBias":
        """Load calibration values from a .npz file."""
        path: Path = GYRO_CALIBRATION_FILEPATH
        if not path.exists():
            logger.warning(f"No calibration data found at {path}")
            return cls(x=0.0, y=0.0, z=0.0)
        data = np.load(path)
        return cls(x=float(data["x"]), y=float(data["y"]), z=float(data["z"]))
