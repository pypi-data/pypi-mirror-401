"""Camera calibration tools for the monocular path prediction pipeline."""

import argparse
from pathlib import Path

from monocular_path_prediction.config.definitions import CameraCalibrationConfig
from monocular_path_prediction.sensors.camera.calibration.calibration import (
    CameraCalibration,
)


def parse_tuple(value: str) -> tuple[int, int]:
    """Parse a comma-separated string into a tuple of ints."""
    try:
        width, height = map(int, value.split(","))
        return width, height
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid tuple: {value}. Expected format WIDTH,HEIGHT."
        ) from e


if __name__ == "__main__":  # pragma: no cover
    """Run the calibration CLI."""
    default_dim = CameraCalibrationConfig.checkerboard_dim
    parser = argparse.ArgumentParser(description="Camera calibration tools.")
    parser.add_argument(
        "--dims",
        "-d",
        type=parse_tuple,
        default=default_dim,
        help=f"Dimensions as WIDTH,HEIGHT (e.g., {default_dim}).",
    )
    parser.add_argument(
        "--images_dir", "-i", help="Path to image folder.", type=Path, default=None
    )
    args = parser.parse_args()

    config = CameraCalibrationConfig(checkerboard_dim=args.dims)
    cal_session = CameraCalibration(config=config)

    if args.images_dir is not None:
        images_dir = args.images_dir
    else:
        images_dir = None
    cal_session.run(images_dir=images_dir)
