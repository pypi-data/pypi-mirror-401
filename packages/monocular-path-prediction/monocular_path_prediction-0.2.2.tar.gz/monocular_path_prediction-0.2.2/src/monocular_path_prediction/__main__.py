"""Monocular Surface Normal Estimation Script."""

import argparse
from pathlib import Path

from monocular_path_prediction.config.definitions import (
    DEFAULT_LOG_LEVEL,
    DEFAULT_STDERR_LEVEL,
    LogLevel,
)
from monocular_path_prediction.pipeline import Pipeline, PipelineConfig


def main(
    image_path: Path | None,
    use_loop: bool,
    camera_index: int | None,
    log_level: str,
    stderr_level: str,
) -> None:
    """Run the main function for the Monocular Surface Normal Estimation script."""
    if image_path is not None:
        camera_index = 0

    config = PipelineConfig(
        camera_index=camera_index,
        hide_display=False,
        log_level=log_level,
        stderr_level=stderr_level,
    )
    pipeline = Pipeline(config=config)
    if use_loop:
        pipeline.run_loop(image_path=image_path)
    else:
        pipeline.run(image_path=image_path)
    pipeline.close()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Monocular Path Planning through Surface Normals."
    )
    parser.add_argument(
        "--image_filepath",
        "-i",
        type=str,
        default=None,
        help="Optional filepath to an input image",
    )
    parser.add_argument(
        "--hide_display",
        help="Hide the visualization display",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--loop",
        help="Run in a loop",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--log-level",
        "-l",
        help="Select the log level",
        required=False,
        choices=list(LogLevel()),
        default=DEFAULT_LOG_LEVEL,
    )
    parser.add_argument(
        "--stderr-level",
        "-s",
        help="Select the std err level",
        required=False,
        choices=list(LogLevel()),
        default=DEFAULT_STDERR_LEVEL,
    )
    parser.add_argument(
        "--camera_index",
        "-c",
        type=int,
        help="Camera index",
        required=False,
        default=None,
    )

    args = parser.parse_args()

    main(
        image_path=args.image_filepath,
        use_loop=args.loop,
        log_level=args.log_level,
        stderr_level=args.stderr_level,
        camera_index=args.camera_index,
    )
