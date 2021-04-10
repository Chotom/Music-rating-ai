import os

import yaml

from data_collection.youtube_api._playlist_processing import download_playlist
from utilities import ROOT_DIR, create_logger, load_yml_settings, dump_datetime, save_yml_settings, SETTINGS_PATH, \
    TMP_DATA_FILEPATH, YOUTUBE_DATA_FILEPATH


def update_youtube_data():
    """
    Update youtube data from defined playlists in settings to csv file
    and save their latest video datetime for next update
    """

    # Init
    log = create_logger('update_youtube_data')
    settings = load_yml_settings(SETTINGS_PATH)
    log.info("Trying to download playlists...")

    # Get data from every playlist
    for playlist_name in settings['playlists']:
        playlist = settings['playlists'][playlist_name]

        # Trying to download descriptions from playlist
        if (latest_video_date := download_playlist(playlist['id'], TMP_DATA_FILEPATH, playlist['date'])) is None:
            log.error(f'error in downloading playlist {playlist["id"]}')
        else:
            playlist['date'] = dump_datetime(latest_video_date)

        # Append tmp file to file with all descriptions
        f = open(YOUTUBE_DATA_FILEPATH, "a", encoding='utf-8', errors="ignore")
        f_tmp = open(TMP_DATA_FILEPATH, "r", encoding='utf-8', errors="ignore")
        f.write(f_tmp.read())
        f_tmp.close()
        f.close()

        # Delete tmp file
        if os.path.exists(TMP_DATA_FILEPATH):
            os.remove(TMP_DATA_FILEPATH)

    save_yml_settings(SETTINGS_PATH, settings)
    log.info("Downloading ended")


def clean_youtube_data():
    """
    Delete youtube data and reset saved datetime in settings
    """

    # Init
    log = create_logger('clean_youtube_data')
    settings = load_yml_settings(SETTINGS_PATH)
    log.info("Trying to clean data...")

    # Reset datetime in every playlist
    for playlist_name in settings['playlists']:
        playlist = settings['playlists'][playlist_name]
        playlist['date'] = ''

        # Delete youtube data file
        if os.path.exists(YOUTUBE_DATA_FILEPATH):
            os.remove(YOUTUBE_DATA_FILEPATH)

    save_yml_settings(SETTINGS_PATH, settings)
    log.info("Cleaning ended")


def show_youtube_settings():
    """
    print consts and used settings
    """

    # Init
    log = create_logger('show_youtube_settings')
    settings = load_yml_settings(SETTINGS_PATH)

    # Print info
    log.info(f'settings path: {SETTINGS_PATH}')
    log.info(f'youtube data path: {YOUTUBE_DATA_FILEPATH}')
    log.info(f'Settings:\n{yaml.dump(settings, default_flow_style=False)}')
