"""Camera tools for the monocular path prediction pipeline."""

from dataclasses import dataclass

from numpy.typing import NDArray


@dataclass
class CameraIntrinsics:
    """Store calibration results.

    :param NDArray camera_matrix: 3x3 intrinsic matrix.
    :param NDArray dist_coeffs: Distortion coefficients.
    :param tuple[int, int] image_size: Image size as (width, height).
    """

    camera_matrix: NDArray
    dist_coeffs: NDArray
    image_size: tuple[int, int]
