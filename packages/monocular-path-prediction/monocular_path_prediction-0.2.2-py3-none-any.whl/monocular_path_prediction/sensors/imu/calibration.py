"""IMU device calibration."""

import numpy as np
from loguru import logger

from monocular_path_prediction.sensors.imu.data_classes import GyroBias, Vector3D


class GyroCalibration:
    """Gyro calibration class."""

    def __init__(self, gyro_data: Vector3D):
        logger.debug("Gyro Calibration")
        self.gyro_data = gyro_data
        self.bias = self.calibrate()

    def calibrate(self) -> GyroBias:
        """Run IMU calibration."""
        logger.debug("Finding gyroscope bias.")
        mu_x = np.mean(self.gyro_data.x)
        mu_y = np.mean(self.gyro_data.y)
        mu_z = np.mean(self.gyro_data.z)
        bias = (mu_x, mu_y, mu_z)
        logger.debug(f"gyro bias: {bias}")
        return GyroBias(x=float(mu_x), y=float(mu_y), z=float(mu_z))

    def save(self) -> None:
        """Save calibration result to disk."""
        logger.debug("Saving calibration.")
        yes_str = "Y"
        no_str = "n"
        if input(f"Overwrite? ({yes_str}/{no_str}) ") == yes_str:
            self.bias.save()
        else:
            logger.info("Calibration values not saved.")
