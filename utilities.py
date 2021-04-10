import yaml
import json
import os
import logging
import requests

from datetime import datetime
from typing import Dict, Optional

# Consts:

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_LEVEL = 'INFO'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
TMP_DATA_FILEPATH = ROOT_DIR + '/data/tmp_playlist.csv'
YOUTUBE_DATA_FILEPATH = ROOT_DIR + "/data/youtube_data.csv"
SETTINGS_PATH = ROOT_DIR + '/data_collection/settings_api.yml'


# Functions:

def create_logger(name: str) -> logging.Logger:
    """
    Create logger for given name

    :param name: name of logger
    :return: logger
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)

    ch = logging.StreamHandler()  # console handler
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    if not len(logger.handlers):
        logger.addHandler(ch)
    return logger


def dump_datetime(date: datetime) -> str:
    """
    Cast datetime to string format '%Y-%m-%dT%H:%M:%SZ'

    :param date: datetime to cast
    :return: datetime as string
    """
    return datetime.strftime(date, '%Y-%m-%dT%H:%M:%SZ')


def get_datetime(date_str: str) -> datetime:
    """
    Cast string from '%Y-%m-%dT%H:%M:%SZ' format to datetime

    :param date_str: string with datetime to cast
    :return: '2000-01-01T00:00:00Z' as default, or casted datetime
    """
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        date_str = '2000-01-01T00:00:00Z'
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return date


def load_yml_settings(load_filepath: str) -> Dict:
    log = create_logger("load_yml_settings")
    try:
        with open(load_filepath, "r") as config_file:
            config = yaml.safe_load(config_file)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise
    return config


def save_yml_settings(save_filepath: str, config: Dict):
    log = create_logger("save_yml_settings")
    try:
        with open(save_filepath, "w") as config_file:
            yaml.dump(config, config_file, default_flow_style=False)
        config_file.close()
    except FileNotFoundError as e:
        log.error("FileNotFoundError: ", e)
        raise


def get_json_response(url: str) -> Optional[Dict]:
    """
    Handle request and return json response as dict

    :param url: url to page
    :return: None on failure, Json response as dict on success
    """
    log = create_logger("get_json_response")

    try:
        response = requests.get(url, HEADERS, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error(f'error occurred during handling {url} url request: {e}')
        return None

    try:
        json_response = json.loads(response.text)
    except json.JSONDecodeError as e:
        log.error(f'error occurred during parsing response from {url} url request: {e}')
        return None

    return json_response
