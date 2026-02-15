import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from beartype import beartype as ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns
    Args:
        path_to_yaml (Path): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty yaml file
    Returns:
        ConfigBox: config box type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    Args:
        path_to_directories (list): list of path of directories to create
        verbose (bool, optional): whether to log info. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Save json data
    Args:
        path (Path): path like input
        data (dict): data to save
    """

    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    logger.info(f"json file saved at path: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load json data
    Args:
        path (Path): path like input
    Returns:
        ConfigBox: config box type
    """

    with open(path) as json_file:
        content = json.load(json_file)
    
    logger.info(f"json file loaded from path: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary data
    Args:
        data (Any): data to save
        path (Path): path like input
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at path: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data
    Args:
        path (Path): path like input
    Returns:
        Any: loaded data
    """
    data = joblib.load(filename=path)
    logger.info(f"binary file loaded from path: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB
    Args:
        path (Path): path like input
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"{size_in_kb} KB"

@ensure_annotations
def decodeImage(imghstring: str, fileName: str) -> Path:
    """Decode base64 string and save as image
    Args:
        imghstring (str): base64 string of image
        fileName (str): name of the file to save
    Returns:
        Path: path to the saved image file
    """
    imgdata = base64.b64decode(imghstring)
    filePath = Path(fileName)
    with open(filePath, 'wb') as f:
        f.write(imgdata)
    logger.info(f"Image decoded and saved at path: {filePath}")
    return filePath

def encodeImage(filePath: Path) -> str:
    """Encode image file to base64 string
    Args:
        filePath (Path): path to the image file
    Returns:
        str: base64 string of the image
    """
    with open(filePath, 'rb') as f:
        imgdata = f.read()
    imghstring = base64.b64encode(imgdata)
    logger.info(f"Image at path: {filePath} encoded to base64 string")
    return imghstring