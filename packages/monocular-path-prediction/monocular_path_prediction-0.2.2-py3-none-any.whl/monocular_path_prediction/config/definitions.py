"""Definitions for the package."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

import numpy as np

np.set_printoptions(precision=3, floatmode="fixed", suppress=True)

GRAVITY = 9.80665  # meters / sec^2

# --- Directories ---
ROOT_DIR: Path = Path("src").parent
DATA_DIR: Path = ROOT_DIR / "data"

RECORDINGS_DIR: Path = DATA_DIR / "recordings"
ERRORS_DIR: Path = RECORDINGS_DIR / "errors"

LOG_DIR: Path = DATA_DIR / "logs"
CALIBRATION_DIR: Path = DATA_DIR / "calibration"

# Default encoding
ENCODING: str = "utf-8"

DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"

SERIAL_DEVICE_PREFIX: str = "/dev/tty.usbmodem"


# Default plot settings
@dataclass
class FigureSettings:
    """Figure settings for matplotlib plots."""

    size: tuple[float, float] = (15, 8.5)  # inches
    alpha: float = 0.8


SPACE_KEY = 32
ESCAPE_KEY = 27

DEFAULT_IMAGE_WIDTH = 832

EPSILON = 1e-8

DISPLAY_ALPHA = 0.6

IMAGE_TYPE = "png"


@dataclass
class LogLevel:
    """Log level."""

    trace: str = "TRACE"
    debug: str = "DEBUG"
    info: str = "INFO"
    success: str = "SUCCESS"
    warning: str = "WARNING"
    error: str = "ERROR"
    critical: str = "CRITICAL"

    def __iter__(self):
        """Iterate over log levels."""
        return iter(asdict(self).values())


DEFAULT_LOG_LEVEL = LogLevel.info
DEFAULT_STDERR_LEVEL = LogLevel.debug


@dataclass
class Colors:
    """Color constants."""

    red: tuple[int, int, int] = (0, 0, 255)
    green: tuple[int, int, int] = (0, 255, 0)
    blue: tuple[int, int, int] = (255, 0, 0)
    yellow: tuple[int, int, int] = (0, 255, 255)
    white: tuple[int, int, int] = (255, 255, 255)
    black: tuple[int, int, int] = (0, 0, 0)
    gray: tuple[int, int, int] = (128, 128, 128)


# settings for the Depth Anything V2 models
PRETRAINED_MODEL_DIR = DATA_DIR / "checkpoints"
MODEL_EXTENSION = ".pth"

GYRO_CALIBRATION_FILEPATH: Path = CALIBRATION_DIR / "gyro_calibration.npz"


class ModelSize(Enum):
    """Available depth estimation model sizes."""

    SMALL = "vits"
    MEDIUM = "vitb"
    LARGE = "vitl"


@dataclass(frozen=True)
class DepthModelConfig:
    """Define the depth estimation model configuration."""

    encoder: str
    features: int
    out_channels: list[int] = field(default_factory=list)


# Predefined model configurations
MODEL_CONFIG_SMALL = DepthModelConfig(
    encoder="vits", features=64, out_channels=[48, 96, 192, 384]
)

MODEL_CONFIG_MEDIUM = DepthModelConfig(
    encoder="vitb", features=128, out_channels=[96, 192, 384, 768]
)

MODEL_CONFIG_LARGE = DepthModelConfig(
    encoder="vitl", features=256, out_channels=[256, 512, 1024, 1024]
)


@dataclass
class IMUFilterConfig:
    """Class for configuring the IMU filter."""

    gain: float = 0.033
    delta_time_sec: float = 0.01


# IMU settings
@dataclass
class IMUReaderConfig:
    """Class for configuring the IMU."""

    time_pattern = r"Time:\s*([0-9.]+)"
    meas_pattern = r"Measurements:\s*(\[.*\])"
    gyro_range_rps: float = 10  # rad / sec
    accel_range_gs: float = 20  # meters / sec ^2
    wait_time_sec: float = 5.0


@dataclass
class SerialConfig:
    """Class for configuring a serial device."""

    port: str = ""
    baud_rate: int = 115200
    timeout: float = 0.1
    encoder: str = ENCODING
    loop_delay: float = 0.001
    # How long to wait in total when trying to open initially
    initial_connect_timeout_s: float = 3.0
    # Backoff when open fails or device disconnects
    retry_backoff_s: float = 0.25
    # Number of open retries before giving up during initial connect
    open_retries: int = int(initial_connect_timeout_s / retry_backoff_s)


@dataclass
class PipelineConfig:
    """Configuration for the pipeline."""

    model_config: DepthModelConfig = MODEL_CONFIG_SMALL
    camera_index: int | None = 0
    imu_config: SerialConfig = field(default_factory=SerialConfig)
    max_point_distance: float = 1.0
    output_dir: Path = RECORDINGS_DIR
    hide_display: bool = False
    log_level: str = DEFAULT_LOG_LEVEL
    stderr_level: str = DEFAULT_STDERR_LEVEL
    save_images: bool = False
    surface_normal_threshold: float = 0.90


@dataclass
class CameraCalibrationConfig:
    """Hold calibration parameters and runtime options.

    Configure the chessboard target, capture behavior, and I/O paths.

    :param checkerboard_dim: tuple[int, int] (cols, rows) of inner corners.
    :param square_size_meters: float Size of a square in meters (or chosen unit).
    :param capture_count: int Number of valid frames to capture.
    :param save_dir: Path Directory to save captured frames.
    :param capture_count_min: int Minimum number of valid frames to capture.
    """

    checkerboard_dim: tuple[int, int] = (6, 9)
    square_size_meters: float = 0.020
    capture_count: int = 15
    save_dir: Path = CALIBRATION_DIR
    capture_count_min: int = 5


IMU_FILENAME_KEY = "imu_data"


class IMUUnits(Enum):
    """Configuration for the IMU."""

    ACCEL = "m/s^2"
    GYRO = "rad/s"
    MAG = "uT"


class IMUDataFileColumns(Enum):
    """Configuration for the IMU data files."""

    TIMESTAMP = "timestamp (sec)"
    ACCEL_X = f"accel_x ({IMUUnits.ACCEL.value})"
    ACCEL_Y = f"accel_y ({IMUUnits.ACCEL.value})"
    ACCEL_Z = f"accel_z ({IMUUnits.ACCEL.value})"
    GYRO_X = f"gyro_x ({IMUUnits.GYRO.value})"
    GYRO_Y = f"gyro_y ({IMUUnits.GYRO.value})"
    GYRO_Z = f"gyro_z ({IMUUnits.GYRO.value})"
    MAG_X = f"mag_x ({IMUUnits.MAG.value})"
    MAG_Y = f"mag_y ({IMUUnits.MAG.value})"
    MAG_Z = f"mag_z ({IMUUnits.MAG.value})"


CAM_TO_WORLD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, -1.0, 0.0],
    ]
)
