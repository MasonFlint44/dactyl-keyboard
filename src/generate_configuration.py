import json
import os
from argparse import ArgumentParser
from typing import Optional

from pydantic import parse_raw_as
from pydantic.json import pydantic_encoder

from .models import GlobalConfig


def save_config(
    config_filename: Optional[str] = None,
    update_filename: Optional[str] = None,
):
    shape_config = GlobalConfig().dict(by_alias=True)
    if update_filename:
        with open(os.path.join("configs", f"{update_filename}.json")) as f:
            data = parse_raw_as(dict, f.read())
            shape_config.update(data)

    if config_filename is None:
        config_path = os.path.join("src", "run_config.json")
    else:
        shape_config["save_dir"] = config_filename
        shape_config["config_name"] = config_filename
        config_path = os.path.join("configs", f"{config_filename}.json")

    with open(config_path, mode="w") as f:
        json.dump(shape_config, f, indent=4, default=pydantic_encoder)


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
