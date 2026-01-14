"""Monocular Surface Normal Estimation Script."""

import sys
import traceback
from collections import deque
from pathlib import Path

import numpy as np
from loguru import logger
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation as Rot

from monocular_path_prediction import MonocularDepthEstimator, PointCloudGenerator
from monocular_path_prediction.config.definitions import (
    CAM_TO_WORLD,
    PipelineConfig,
)
from monocular_path_prediction.config.setup_logger import setup_logger
from monocular_path_prediction.path_planner import PathPlanner
from monocular_path_prediction.sensors.camera.camera import Camera
from monocular_path_prediction.sensors.camera.display import Display
from monocular_path_prediction.sensors.camera.images.images import (
    load_image,
    save_failed_image,
)
from monocular_path_prediction.sensors.imu import IMUDevice, Vector3D
from monocular_path_prediction.sensors.setup import setup_camera, setup_imu


class Pipeline:
    """Main class for running monocular surface normal estimation."""

    def __init__(self, config: PipelineConfig):
        self.log_filepath: Path = setup_logger(
            filename="pipeline",
            stderr_level=config.log_level,
            log_level=config.log_level,
        )
        logger.info("Setting up pipeline...")

        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        self.depth_estimator = MonocularDepthEstimator(self.config.model_config)
        self.camera: Camera = setup_camera(camera_index=self.config.camera_index)
        if self.camera.calibration is None:
            msg = "Calibration not available."
            logger.error(msg)
            raise RuntimeError(msg)
        self.imu: IMUDevice = setup_imu(imu_config=self.config.imu_config)
        self.display: Display = Display()

        self._gyro_history: deque[Vector3D] = deque(maxlen=20)

        # TODO - add microcontroller setup
        logger.info("Pipeline setup complete.")

    def run_loop(self, image_path: Path | None = None) -> None:
        """Run the pipeline in a loop.

        :param image_path: The path to the image to process.
        :return: None
        """
        logger.info("Running pipeline in loop... Press Ctrl+C to exit.")
        while True:
            try:
                self.run(image_path=image_path)
            except KeyboardInterrupt:
                logger.info("Pipeline interrupted.")
                break
            except Exception as err:
                logger.error(f"Pipeline failed: {err}")

    def run(self, image_path: Path | None) -> bool:
        """Run the pipeline.

        :param image_path: The path to the image to process.
        :return: bool True if the pipeline was successful.
        """
        logger.debug("Running pipeline iteration.")
        image = None
        try:
            if self.imu is None:
                msg = "No IMU device configured."
                logger.warning(msg)
                return False

            imu_data, imu_pose = self.imu.wait_for_data()
            logger.debug(f"IMU device is ready: {imu_data[0]}")

            gyro_world_frame = imu_data[0].gyro.rotate(imu_pose[0].T)
            self._gyro_history.append(gyro_world_frame)

            # load image from file path if it exists or take a picture
            if image_path:
                image = load_image(image_path)
            else:
                image = self.camera.capture_frame()
            if image is None:
                logger.warning("Failed to capture frame.")
                return False
            self.display.add_frame(frame=image)

            run_algo = True
            if run_algo:
                depth_map = self.depth_estimator.infer_depth(image)

                self.display.add_depth_map(
                    depth_map=depth_map, max_distance=self.config.max_point_distance
                )
                self._run_algorithm(depth_map=depth_map, camera_pose=imu_pose[0])

                self.display.add_pose(pose=imu_pose[0])
                self.display.add_frame_rate()

                if not self.config.hide_display:
                    self.display.show()

            if self.config.save_images:
                self.display.save(output_dir=self.config.output_dir)

            return True

        except OSError as err:
            logger.error(f"Pipeline exiting: {err}")
            self.close()
            sys.exit(1)
        except Exception as err:
            logger.warning(f"Pipeline failed: {err}")
            logger.error("--- Full traceback ---")
            traceback.print_exc()
            if image is not None:
                save_failed_image(image=image)
            return False

    def _run_algorithm(self, depth_map: NDArray, camera_pose: NDArray) -> None:
        """Run the pipeline algorithm."""
        point_cloud = PointCloudGenerator.from_depth_map(
            depth_map=depth_map, camera_cal=self.camera.calibration
        )
        point_cloud.filter_by_distance(self.config.max_point_distance)

        random_sample = False
        if random_sample:
            point_cloud.random_subsample(num_samples=10000)
        else:
            point_cloud.down_sample(stride=19)

        camera_pose_no_yaw = remove_z_component(pose=camera_pose)

        rotation = camera_pose_no_yaw @ CAM_TO_WORLD
        point_cloud.rotate(rotation_matrix=rotation)

        point_cloud.filter_by_normals(threshold=self.config.surface_normal_threshold)
        point_cloud.filter_by_height(height=1.0)

        planner = PathPlanner(
            point_cloud=point_cloud, gyro_history=self.get_gyro_history_stats()
        )
        path = planner.get_path_best()
        logger.debug(f"Path median:\n{path}")

        # convert back to camera frame
        point_cloud.rotate(rotation_matrix=rotation.T)
        uv = point_cloud.project_points(K=self.camera.calibration)
        self.display.draw_points(points=uv)

        path.rotate(rotation_matrix=rotation.T)
        uv = path.project_points(K=self.camera.calibration)

        u, v = uv.T
        self.display.draw_line(uv=(u, v))

    def close(self) -> None:
        """Close all resources cleanly."""
        logger.info("Shutting down pipeline...")
        if self.imu:
            self.imu.close()
        if self.camera:
            self.camera.cleanup()
        logger.success("Pipeline closed.")

    def get_gyro_history(self) -> NDArray:
        """Get the gyro history.

        :return: gyro history
        """
        logger.debug("Getting gyro history as a numpy array.")
        return np.vstack(tuple(val.as_array() for val in self._gyro_history))

    def get_gyro_history_stats(self) -> tuple[NDArray, NDArray]:
        """Get the gyro history."""
        gyro_history = self.get_gyro_history()
        mean = np.mean(gyro_history, axis=1)
        var = np.var(gyro_history, axis=1)

        logger.debug(f"gyro mean: {mean}")
        logger.debug(f"gyro var: {var}")

        return mean, var


def remove_z_component(pose: NDArray) -> NDArray:
    """Remove the z-component from the pose."""
    roll, pitch, _ = Rot.from_matrix(pose).as_euler(seq="xyz", degrees=False)
    pose_new = Rot.from_euler(
        angles=[float(roll), float(pitch), 0.0], seq="xyz", degrees=False
    ).as_matrix()
    return pose_new
