import argparse
import os
from os import path
from typing import Any, Dict, Optional

from pydantic import parse_raw_as

from .models import GlobalConfig


def make_dactyl(config: GlobalConfig, save_path: str):
    right_cluster: Optional[str] = None
    left_cluster: Optional[str] = None

    def cluster(side: str = "right") -> Optional[str]:
        return right_cluster if side == "right" else left_cluster

    config_data = {**shape_config, **config.dict()}

    if config.save_name:
        config_name = config.save_name
    elif config.overrides:
        config_name = (
            f"{config.overrides}_{config.nrows}x{config.ncols}_{config.thumb_style}"
        )

    if config.engine:
        print(f"Found Current Engine in Config = {config.engine}")
    else:
        print("Engine Not Found in Config")
        config.engine = "solid"
        print(f"Setting Current Engine = {config.engine}")

    parts_path = os.path.abspath(path.join("src", "parts"))

    if config.save_dir not in ["", None, "."]:
        save_path = config.save_dir
        print(f"save_path set to save_dir json setting: {save_path}")

    dir_exists = os.path.isdir(save_path)
    if not dir_exists:
        os.makedirs(save_path, exist_ok=True)


def merge_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    if not (overrides := config.get("overrides")):
        return config
    with open(path.join(config.get("save_path", "."), f"{overrides}.json")) as f:
        override_data = parse_raw_as(dict, f.read())
    return {**config, **override_data}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Specify configuration file")
    parser.add_argument("--save_path", help="Specify save path", default=".")
    args = parser.parse_args()

    if args.config:
        config_path = os.path.join("configs", f"{args.config}.json")
    else:
        print("NO CONFIGURATION SPECIFIED, USING run_config.json")
        config_path = os.path.join("src", "run_config.json")

    with open(config_path) as f:
        shape_config = parse_raw_as(GlobalConfig, f.read()).dict(by_alias=True)

    if args.save_path:
        print(f"save_path set to argument: {args.save_path}")

    # merge overrides into shape_config
    shape_config = merge_overrides(shape_config)

    make_dactyl(GlobalConfig(**shape_config), args.save_path)
