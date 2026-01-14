"""Path planner module from point cloud and gyro history."""

import numpy as np
from loguru import logger
from numpy.typing import NDArray

from monocular_path_prediction.data.point_cloud import PointCloudData


class PathPlanner:
    """Path planner class."""

    def __init__(
        self, point_cloud: PointCloudData, gyro_history: tuple[NDArray, NDArray]
    ):
        """Initialize the PathPlanner class."""
        self.point_cloud = point_cloud
        self.gyro_history = gyro_history
        self.step_distance = 0.05

    def get_path(self) -> PointCloudData:
        """Predict a path from the point cloud."""
        logger.debug("Finding path through point cloud...")
        min_xyz = np.min(self.point_cloud.points, axis=0)
        max_xyz = np.max(self.point_cloud.points, axis=0)

        mean, _ = self.gyro_history
        mean = mean / 100.0

        weighting = np.linspace(0.01, 2, len(mean))
        mean *= weighting
        mean = mean / np.nanmean(weighting)
        mean = np.nanmean(mean)

        distances = np.arange(
            start=min_xyz[1], stop=max_xyz[1], step=self.step_distance
        )
        path = np.zeros(shape=(len(distances), 3))
        for idx, dist in enumerate(distances):
            points = self.point_cloud.filter_by_plane(
                plane=(0.0, 1.0, 0.0, -float(dist)), max_distance=4 * self.step_distance
            )
            med = np.median(points, axis=0)
            path[idx, :] = med

            path[idx, 0] = -np.clip(idx**2 * mean * 2, a_min=-0.1, a_max=0.1)

        # check for large gaps
        path_norm = np.linalg.norm(path, axis=1)
        diff_path = np.diff(path_norm)
        for idx, dist in enumerate(diff_path):
            if dist > 10 * self.step_distance:
                path = path[0:idx, :]
                break

        return PointCloudData(points=path)

    def get_path_median(self) -> PointCloudData:
        """Predict a median path through the point cloud."""
        logger.debug("Finding median path through point cloud...")
        min_xyz = np.min(self.point_cloud.points, axis=0)
        max_xyz = np.max(self.point_cloud.points, axis=0)

        distances = np.arange(
            start=min_xyz[1], stop=max_xyz[1], step=self.step_distance
        )
        path = np.zeros(shape=(len(distances), 3))
        for idx, dist in enumerate(distances):
            points = self.point_cloud.filter_by_plane(
                plane=(0.0, 1.0, 0.0, -float(dist)), max_distance=2 * self.step_distance
            )
            med = np.median(points, axis=0)
            path[idx, :] = med

        return PointCloudData(points=path)

    def get_path_best(self) -> PointCloudData:
        """Predict a smart path through the point cloud."""
        logger.debug("Finding best path through point cloud...")
        min_xyz = np.min(self.point_cloud.points, axis=0)
        max_xyz = np.max(self.point_cloud.points, axis=0)
        mask_1 = np.linalg.norm(self.point_cloud.points, axis=1) < 0.1
        mask_2 = np.linalg.norm(self.point_cloud.points, axis=1) > 0.05
        mask = np.logical_and(mask_1, mask_2)
        points = self.point_cloud.points[mask, :]
        logger.debug(f"Point shape: {points.shape}")

        distances = np.arange(
            start=min_xyz[1], stop=max_xyz[1], step=self.step_distance
        )
        path = np.zeros(shape=(len(distances), 3))

        # find the path
        dist = distances[0]
        points = self.point_cloud.filter_by_plane(
            plane=(0.0, 1.0, 0.0, -float(dist)), max_distance=2 * self.step_distance
        )
        med = np.median(points, axis=0)
        path[0, :] = med

        for idx, dist in enumerate(distances):
            points = self.point_cloud.filter_by_plane(
                plane=(0.0, 1.0, 0.0, -float(dist)), max_distance=2 * self.step_distance
            )
            med = np.median(points, axis=0)
            path[idx, :] = med

        return PointCloudData(points=path)
