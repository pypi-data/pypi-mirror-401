"""Camera interface for recording and taking pictures using OpenCV."""

from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from numpy.typing import NDArray
from PIL import Image

from monocular_path_prediction.config.definitions import ERRORS_DIR, IMAGE_TYPE
from monocular_path_prediction.sensors.camera.camera_intrinsics import CameraIntrinsics
from monocular_path_prediction.utils import create_timestamped_filepath


def resize_image(image: NDArray, new_width: int) -> NDArray:
    """Resize an image to a target width while maintaining the same aspect ratio.

    Args:
        image: Input image as a numpy array
        new_width: Target width in pixels

    Returns:
        resized_image

    """
    h, w = image.shape[:2]
    scale_factor = new_width / w
    new_height = int(h * scale_factor)

    # Convert numpy array to PIL Image for resizing
    pil_image = Image.fromarray(image)
    resized_pil = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_image = np.array(resized_pil)

    logger.debug(f"Image resized to {resized_image.shape}")

    return resized_image


def undistort_image(image: NDArray, calib: CameraIntrinsics | None) -> NDArray:
    """Return an undistorted copy of an image using the calibration.

    :param NDArray image: Input distorted image.
    :param CameraIntrinsics calib: Calibration results with intrinsics and distortion.
    :return: Undistorted image of the same size.
    :rtype: NDArray
    """
    if calib is None:
        logger.warning("Calibration not available")
        return image.copy()
    h, w = image.shape[:2]
    new_camera_mtx, _ = cv2.getOptimalNewCameraMatrix(
        calib.camera_matrix, calib.dist_coeffs, (w, h), 1, (w, h)
    )
    return cv2.undistort(
        image, calib.camera_matrix, calib.dist_coeffs, None, new_camera_mtx
    )


def load_image(image_path: Path) -> NDArray:
    """Load an image from the given path."""
    logger.debug(f"Loading image from {image_path}")
    return np.array(Image.open(str(image_path)))


def list_images(directory: str | Path) -> list[Path]:
    """Return a list of image file paths in the given directory."""
    directory = Path(directory)
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

    return [
        file for file in directory.iterdir() if file.suffix.lower() in image_extensions
    ]


def save_failed_image(image: NDArray) -> None:
    """Save an image from the given path.

    :param NDArray image: Input image.
    :return: None
    """
    filepath = create_timestamped_filepath(
        output_dir=ERRORS_DIR, suffix=IMAGE_TYPE, prefix="error"
    )
    cv2.imwrite(filename=str(filepath), img=image)
