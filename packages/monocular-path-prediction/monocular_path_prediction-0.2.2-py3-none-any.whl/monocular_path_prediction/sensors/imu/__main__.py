"""Main file for testing the IMU device."""

import argparse
import time

from loguru import logger

from monocular_path_prediction.sensors.imu.calibration import GyroCalibration
from monocular_path_prediction.sensors.imu.filter import (
    process_imu_data_frame_with_filter,
)
from monocular_path_prediction.sensors.imu.plotter import plot_imu_data
from monocular_path_prediction.sensors.imu.reader import load_imu_data
from monocular_path_prediction.sensors.setup import setup_imu

if __name__ == "__main__":  # pragma: no cover
    """Test the IMU device."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true", help="Record IMU data")
    args = parser.parse_args()

    imu = setup_imu(imu_config=None, record_data=args.record)
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        logger.info("Interrupted.")
    finally:
        imu.close()

    if imu.data_recorder is not None:
        imu.data_recorder.save_dataframe()
        imu_data_frame = load_imu_data(filepath=imu.data_recorder.filepath)
        gyro_calibration = GyroCalibration(gyro_data=imu_data_frame.gyros[0])
        gyro_calibration.save()
        quaternions = process_imu_data_frame_with_filter(imu_data_frame=imu_data_frame)
        plot_imu_data(imu_data_frame=imu_data_frame, quaternions=quaternions)
