"""Displayer to show camera frames."""

from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation as Rot

from monocular_path_prediction.config.definitions import (
    DISPLAY_ALPHA,
    IMAGE_TYPE,
    Colors,
)
from monocular_path_prediction.utils import LoopTimer, create_timestamped_filepath


def get_color_fade(steps: int, idx: int) -> tuple[float, float, float]:
    """Get a color that fades from white to black."""
    color = 255 - idx * 255 / steps

    return color, color, color


class Display:
    """Display camera frames."""

    def __init__(self, window_name: str = "Camera Display") -> None:
        super().__init__()
        self.timer: LoopTimer = LoopTimer()
        self.window_name: str = window_name
        self.frame: NDArray = np.array([])

    def add_frame(self, frame: NDArray | None) -> None:
        """Add a frame to the display."""
        if frame is None:
            logger.warning("No frame provided.")
            return
        self.frame = frame.copy()

    def show(self) -> None:
        """Show the frame."""
        cv2.imshow(self.window_name, self.frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.destroyWindow(self.window_name)

    def add_frame_rate(self) -> None:
        """Add delta time to the frame."""
        if self.frame is None:
            return
        delta_time = self.timer.delta_time_sec()
        if delta_time is None:
            text = "Frame rate: N/A fps"
        else:
            text = f"Frame rate: {1 / delta_time:.1f} fps"
        font = cv2.FONT_HERSHEY_SIMPLEX
        location = (10, 30)
        cv2.putText(
            self.frame,
            text,
            location,
            font,
            fontScale=0.7,
            color=Colors.red,
            thickness=1,
        )
        return

    def add_pose(self, pose: NDArray | None) -> None:
        """Add pose to the frame."""
        if self.frame is None:
            return
        if pose is None:
            logger.debug("No pose specified. Skipping frame.")
            return
        if pose.shape != (3, 3):
            logger.warning(f"Pose has invalid shape {pose.shape}; expected (3, 3).")
            return

        unit_axes = False
        if unit_axes:
            self._add_unit_axes(pose=pose)
        else:
            pilot = PilotDisplay(pose=pose, frame=self.frame)
            self.frame = pilot.frame

        return

    def _add_unit_axes(self, pose: NDArray) -> None:
        """Add unit axes to the frame."""
        length_pixels = 75
        axes = pose * float(length_pixels)

        height_pixels = np.shape(self.frame)[0]
        width_pixels = np.shape(self.frame)[1]
        origin_x = int(width_pixels - length_pixels)
        origin_y = int(height_pixels - length_pixels)
        origin = (origin_x, origin_y)

        # Project the unit axes onto the camera frame
        for idx_xyz, color in enumerate([Colors.red, Colors.green, Colors.blue]):
            ax_x, ax_z = axes[0, idx_xyz], axes[2, idx_xyz]  # Project to the x-z plane
            ax = (int(origin_x - ax_x), int(origin_y - ax_z))
            cv2.line(img=self.frame, pt1=ax, pt2=origin, color=color, thickness=2)
        cv2.circle(self.frame, origin, 3, Colors.yellow, -1)

    def add_depth_map(self, depth_map: NDArray, max_distance: float) -> None:
        """Add depth map to the display."""
        if self.frame is None:
            return

        depth_mask = (depth_map > 0.0) & (depth_map < max_distance)

        # Convert base image to BGR for OpenCV display
        img_bgr = cv2.cvtColor(self.frame.copy(), cv2.COLOR_RGB2BGR).copy()

        # Normalize depth on the masked region (avoid NaNs / empty mask)
        masked_vals = depth_map[depth_mask]
        if masked_vals.size > 0:
            d_min = float(np.nanmin(masked_vals))
            d_max = float(np.nanmax(masked_vals))
            if np.isfinite(d_min) and np.isfinite(d_max) and d_max > d_min:
                depth_norm = (depth_map - d_min) / (d_max - d_min)
            else:
                depth_norm = np.zeros_like(depth_map, dtype=np.float32)
        else:
            depth_norm = np.zeros_like(depth_map, dtype=np.float32)

        # Map to 8-bit and apply colormap
        a_min, a_max = 0, 2**8 - 1
        depth_u8 = np.clip(depth_norm * a_max, a_min, a_max).astype(np.uint8)
        depth_color_bgr = cv2.applyColorMap(depth_u8, cv2.COLORMAP_TURBO)

        # Alpha blend ONLY where mask is true
        m3 = np.repeat(depth_mask[:, :, None], 3, axis=2)
        self.frame[m3] = (
            DISPLAY_ALPHA * depth_color_bgr[m3] + (1.0 - DISPLAY_ALPHA) * img_bgr[m3]
        ).astype(np.uint8)

    def draw_points(self, points: NDArray) -> None:
        """Draw 3D points on the display frame."""
        logger.debug("Drawing points on display.")
        us = points[:, 0]
        vs = points[:, 1]
        for u, v in zip(us, vs, strict=False):
            point = (int(u), int(v))
            cv2.circle(self.frame, point, 0, Colors.white, 1)

    def save(self, output_dir: Path, prefix: str = "display") -> Path:
        """Save an image to a file."""
        filepath = create_timestamped_filepath(
            output_dir=output_dir, suffix=IMAGE_TYPE, prefix=prefix
        )
        cv2.imwrite(filename=str(filepath), img=self.frame)
        logger.info(f"Display saved to: '{filepath}'.")
        return filepath

    def draw_line(self, uv: tuple[NDArray, NDArray]) -> None:
        """Draw line on an OpenCV image."""
        logger.trace("Drawing line on image.")
        if uv is not None:
            u, v = uv
            steps = len(u)
            for i in range(steps - 1):
                pt1 = (int(u[i]), int(v[i]))
                pt2 = (int(u[i + 1]), int(v[i + 1]))
                try:
                    color = get_color_fade(steps=steps, idx=i)
                    cv2.line(self.frame, pt1, pt2, color=color, thickness=5)
                except cv2.error as err:
                    logger.error(
                        f"Failed to draw line on image: {err} - pt1={pt1}, pt2={pt2}."
                    )
                    pass


class PilotDisplay:
    """Draw orientation around the camera."""

    def __init__(self, frame, pose: NDArray):
        """Initialize the display."""
        logger.debug("Initializing PilotDisplay.")
        self.frame = frame

        height_pixels, width_pixels, _ = np.shape(self.frame)
        self.center = (int(width_pixels / 2), int(height_pixels / 2))

        pitch, roll, yaw = Rot.from_matrix(pose).as_euler("xyz", degrees=False)
        self.roll, self.pitch, self.yaw = roll, pitch, yaw

        self.thickness = 1
        self.radius = 11

        self.color = Colors.green

        self.add_roll()
        self.add_yaw()

    def add_roll(self) -> None:
        """Add the roll angle to the visualization."""
        self._draw_horizon()
        self._draw_vertical()

    def _draw_horizon(self) -> None:
        """Add pilot orientation to the frame."""
        _, width_pixels, _ = np.shape(self.frame)

        dist = width_pixels / 4
        for direction in [1, -1]:
            pt1 = (
                int(direction * dist * np.cos(self.roll) + self.center[0]),
                int(direction * dist * np.sin(self.roll) + self.center[1]),
            )
            pt2 = (
                int(self.center[0] + direction * 4 * self.radius * np.cos(self.roll)),
                int(self.center[1] + direction * 4 * self.radius * np.sin(self.roll)),
            )
            cv2.line(
                self.frame,
                pt1=pt1,
                pt2=pt2,
                color=self.color,
                thickness=self.thickness,
            )
        cv2.circle(
            self.frame,
            center=(self.center[0], self.center[1]),
            radius=self.radius,
            color=self.color,
            thickness=self.thickness,
        )

    def _draw_vertical(self) -> None:
        """Draw vertical line to help visualize the roll angle."""
        dist = 10
        pt1 = (
            int(dist * np.sin(self.roll) + self.center[0]),
            int(dist * -np.cos(self.roll) + self.center[1]),
        )
        pt2 = (
            int(self.center[0] + 4 * self.radius * np.sin(self.roll)),
            int(self.center[1] + 4 * self.radius * -np.cos(self.roll)),
        )
        cv2.line(
            self.frame,
            pt1=pt1,
            pt2=pt2,
            color=self.color,
            thickness=self.thickness,
        )

    def add_yaw(self) -> None:
        """Add yaw to the camera display."""
        height_pixels, _, _ = np.shape(self.frame)
        font = cv2.FONT_HERSHEY_SIMPLEX

        yaw_deg = np.rad2deg(self.yaw)

        spacing = 10
        for ang in np.arange(-180, 180, spacing):
            location = (
                int((ang - yaw_deg) * 20 + self.center[0] + 5),
                height_pixels - 10,
            )

            cv2.putText(
                self.frame,
                text=str(ang),
                org=location,
                fontFace=font,
                fontScale=0.5,
                color=Colors.green,
                thickness=self.thickness,
            )
