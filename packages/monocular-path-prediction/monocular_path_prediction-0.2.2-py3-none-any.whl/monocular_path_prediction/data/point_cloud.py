"""Point cloud generation utilities."""

from dataclasses import dataclass

import cv2
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm

from monocular_path_prediction.config.definitions import FigureSettings
from monocular_path_prediction.sensors.camera.camera_intrinsics import CameraIntrinsics


@dataclass
class PointCloudData:
    """Class for storing point cloud data."""

    points: NDArray  # Shape: (N, 3)

    def filter_by_distance(self, max_distance: float) -> None:
        """Return a subset of points and colors within the specified distance."""
        distances = np.linalg.norm(self.points, axis=1)
        mask = distances < max_distance
        self.points = self.points[mask, :]

    def down_sample(self, stride: int) -> None:
        """Downsample the point cloud using a stride."""
        self.points = self.points[::stride, :]

    def random_subsample(self, num_samples: int, seed: int | None = None) -> None:
        """Randomly subsample points from an array.

        Args:
            num_samples: Number of points to keep (must be <= N).
            seed: Optional random seed for reproducibility.

        Returns:
            Subsampled array of shape (num_samples, D).

        """
        N = np.shape(self.points)[0]
        if num_samples > N:
            raise ValueError(f"num_samples ({num_samples}) > number of points ({N})")

        rng = np.random.default_rng(seed)
        indices = rng.choice(N, size=num_samples, replace=False)
        self.points = self.points[indices]

    def rotate(self, rotation_matrix: NDArray) -> None:
        """Rotate the point cloud using a rotation matrix."""
        logger.debug(f"Rotating point cloud by:\n{rotation_matrix}")
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            points_tran = rotation_matrix @ self.points.T
        self.points = points_tran.T

    def estimate_normals(self, k: int = 20) -> NDArray:
        """Estimate surface normals from point cloud."""
        logger.debug(f"Estimating surface normals with '{k}' neighboring points.")
        neighbors = NearestNeighbors(n_neighbors=k + 1, algorithm="kd_tree").fit(
            self.points
        )
        _, indices = neighbors.kneighbors(self.points)

        normals = np.zeros_like(self.points)

        for i, neighbors in tqdm(
            enumerate(indices),
            total=len(self.points),
            desc="Estimating Normals",
            leave=False,
        ):
            neighbor_pts = self.points[neighbors[1:], :]
            centroid = neighbor_pts.mean(axis=0)
            centered = neighbor_pts - centroid
            cov = centered.T @ centered
            _, _, vh = np.linalg.svd(cov)
            normal = vh[-1]
            normal /= np.linalg.norm(normal)

            # Flip normals to face toward the sensor
            to_sensor = -self.points[i, :]
            if np.dot(normal, to_sensor) < 0:
                normal *= -1

            normals[i] = normal

        return normals

    def plot(self) -> None:
        """Plot the point cloud using matplotlib."""
        fig = plt.figure(figsize=FigureSettings.size)
        ax = fig.add_subplot(111, projection="3d")
        x, y, z = self.points.T

        ax.scatter(x, y, z, c=z, cmap="viridis", s=2)  # s=dot size
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

    def filter_by_plane(
        self,
        plane: tuple[float, float, float, float],
        max_distance: float,
    ) -> NDArray:
        """Filter all points within a given absolute distance of a plane.

        Args:
            plane: (a, b, c, d) coefficients of plane ax + by + cz + d = 0.
            max_distance: Maximum absolute distance (in same units as points).

        Returns:
            Subset of points (M, 3) within the distance.

        """
        a, b, c, d = plane
        normal = np.array([a, b, c], dtype=np.float64)
        norm = np.linalg.norm(normal)
        if norm == 0:
            raise ValueError("Plane normal cannot be zero.")

        # Compute signed distances
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            distances = (self.points @ normal + d) / norm

        mask = np.abs(distances) <= max_distance
        return self.points[mask, :]

    def project_points(self, K: CameraIntrinsics | None) -> NDArray:
        """Project 3D points to 2D pixels.

        :param K: Camera intrinsics.
        :return: Pixel coordinates of shape (N, 2) as float64.
        """
        if K is None:
            msg = "Camera Intrinsics not available."
            logger.error(msg)
            raise RuntimeError(msg)

        pts = np.ascontiguousarray(self.points, dtype=np.float64).reshape(-1, 1, 3)
        r_vec = np.array([0.0, 0.0, 0.0])
        t_vec = np.array([0.0, 0.0, 0.0])
        t_vec = np.ascontiguousarray(t_vec, dtype=np.float64).reshape(3, 1)
        img_pts, _ = cv2.projectPoints(
            pts, r_vec, t_vec, K.camera_matrix, K.dist_coeffs
        )

        return img_pts.reshape(-1, 2)

    def filter_by_normals(self, threshold: float) -> None:
        """Filter point cloud according to the surface normal orientation."""
        normals = self.estimate_normals()
        z_axis = 2
        vertical_mask = np.abs(normals[:, z_axis]) > threshold
        self.points = self.points[vertical_mask, :]

    def filter_by_height(self, height: float = 0.0) -> None:
        """Filter point cloud according to the z axis height."""
        mask = self.points[:, 2] < height
        self.points = self.points[mask, :]


class PointCloudGenerator:
    """Class for generating point clouds from inverse depth maps and images."""

    @staticmethod
    def from_depth_map(
        depth_map: NDArray, camera_cal: CameraIntrinsics | None
    ) -> PointCloudData:
        """Generate point cloud from the inverse depth map and image."""
        logger.debug("Creating point cloud from depth map.")
        if camera_cal is None:
            msg = "Camera Intrinsics not available."
            logger.error(msg)
            raise RuntimeError(msg)

        valid = np.isfinite(depth_map) & (depth_map > 0)

        fx = camera_cal.camera_matrix[0, 0]
        fy = camera_cal.camera_matrix[1, 1]
        cx = camera_cal.camera_matrix[0, 2]
        cy = camera_cal.camera_matrix[1, 2]

        v, u = np.indices(np.shape(depth_map))  # v=row (y), u=col (x), each (H, W)

        Z = depth_map[valid]
        X = (u[valid] - cx) * Z / fx
        Y = (v[valid] - cy) * Z / fy
        points_3d = np.stack((X, Y, Z), axis=-1).reshape(-1, 3)

        return PointCloudData(points=points_3d)
