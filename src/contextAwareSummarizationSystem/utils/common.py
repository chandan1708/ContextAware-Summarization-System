import os
from box.exceptions import BoxValueError
import yaml
from src.contextAwareSummarizationSystem.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, Dict

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns it as a ConfigBox.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory: {path}")

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in bytes.
    """
    size_in_kb=round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"