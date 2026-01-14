"""Test that a serial device is working."""

import sys
import time

from loguru import logger

from monocular_path_prediction.config.definitions import SerialConfig
from monocular_path_prediction.sensors.device.device_selector import Selector
from monocular_path_prediction.sensors.device.serial_device import (
    SerialDevice,
    find_serial_devices,
)

if __name__ == "__main__":  # pragma: no cover
    selector = Selector()
    device_info = selector.select_interactive(device_finder=find_serial_devices)
    cfg = SerialConfig(port=device_info.name)
    try:
        with SerialDevice(cfg) as sd:
            while True:
                logger.info(f"[latest] {sd.latest_line()}")
                time.sleep(0.01)
    except KeyboardInterrupt:
        sys.exit(0)
