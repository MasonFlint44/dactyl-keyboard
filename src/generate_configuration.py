import json
import os
from argparse import ArgumentParser

from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder

from .models import *


def save_config(
    config_filename: Optional[str] = None,
    update_filename: Optional[str] = None,
):
    config = {
        **EngineConfig().dict(),
        **ShapeConfig().dict(),
        **ThumbConfig().dict(),
        **TrackballInWallConfig().dict(),
        **TrackballJsConfig().dict(),
        **TrackballCjConfig().dict(),
        **TrackballConfig().dict(),
        **ExperimentalConfig().dict(),
        **FixedColumnStyleConfig().dict(),
        **SwitchHoleConfig().dict(),
        **OledMountConfig().dict(),
        **ControllerMountConfig().dict(),
        **BottomPlateConfig().dict(),
        **PlateHolesConfig().dict(),
        **PcbConfig().dict(),
    }

    if update_filename:
        with open(os.path.join("..", "configs", f"{update_filename}.json")) as f:
            data = parse_raw_as(dict, f.read())
            config.update(data)

    if config_filename is None:
        config_path = os.path.join(".", "run_config.json")
    else:
        config["save_dir"] = config_filename
        config["config_name"] = config_filename
        config_path = os.path.join("..", "configs", f"{config_filename}.json")

    with open(config_path, mode="w") as f:
        json.dump(config, f, indent=4, default=pydantic_encoder)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config", help="Specify the configuration name and save directory"
    )
    parser.add_argument(
        "--update", help="Update the configuration with the specified file"
    )
    args = parser.parse_args()

    save_config(config_filename=args.config, update_filename=args.update)
