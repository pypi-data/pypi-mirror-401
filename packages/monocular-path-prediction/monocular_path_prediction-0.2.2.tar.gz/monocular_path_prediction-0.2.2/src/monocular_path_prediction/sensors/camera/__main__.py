"""Run the module to test out a camera."""

import cv2
from loguru import logger

from monocular_path_prediction.config.definitions import RECORDINGS_DIR
from monocular_path_prediction.sensors.camera.display import Display
from monocular_path_prediction.sensors.setup import setup_camera

if __name__ == "__main__":  # pragma: no cover
    camera = setup_camera(camera_index=None)
    displayer = Display("Camera Display")
    run_app = True
    try:
        while run_app:
            frame = camera.capture_frame()
            displayer.add_frame(frame)

            key = cv2.waitKey(1)
            if key == ord(" "):
                displayer.save(output_dir=RECORDINGS_DIR)

            displayer.add_frame_rate()
            displayer.show()

    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
    finally:
        camera.cleanup()
        cv2.destroyAllWindows()
