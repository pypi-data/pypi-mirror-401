"""Utility methods to set up sensors."""

from loguru import logger

from monocular_path_prediction.config.definitions import SerialConfig
from monocular_path_prediction.sensors.camera import Camera, map_cameras_to_indices
from monocular_path_prediction.sensors.device.device_info import DeviceInfo
from monocular_path_prediction.sensors.device.device_selector import Selector
from monocular_path_prediction.sensors.device.serial_device import (
    SerialDevice,
    find_serial_devices,
)
from monocular_path_prediction.sensors.imu import IMUDevice


def setup_imu(imu_config: SerialConfig | None, record_data: bool = False) -> IMUDevice:
    """Set up the IMU device."""
    logger.info("Setting up IMU device.")
    if imu_config is None:
        imu_config = SerialConfig()
    imu_picker = Selector()
    imu_info = imu_picker.select_interactive(device_finder=find_serial_devices)
    imu_config.port = imu_info.name
    return IMUDevice(config=imu_config, record_data=record_data)


def setup_serial(serial_config: SerialConfig | None) -> SerialDevice:
    """Set up the IMU device."""
    logger.info("Setting up serial device.")
    if serial_config is None:
        serial_config = SerialConfig()
    serial_picker = Selector()
    serial_info = serial_picker.select_interactive(device_finder=find_serial_devices)
    serial_config.port = serial_info.name
    return SerialDevice(config=serial_config)


def setup_camera(camera_index: int | None) -> Camera:
    """Set up the camera."""
    logger.info("Setting up camera device.")
    if camera_index is None:
        logger.info("Camera index is none. Selecting camera interactively.")
        cam_picker = Selector()
        camera_info = cam_picker.select_interactive(
            device_finder=map_cameras_to_indices
        )
    else:
        logger.info(f"Using camera index: {camera_index}")
        camera_info = DeviceInfo(index=camera_index, name="camera")

    if camera_info is None:
        msg = "No camera selected."
        logger.critical(msg)
        raise RuntimeError(msg)

    return Camera(info=camera_info)
