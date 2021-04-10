import os
import csv

from datetime import datetime
from typing import Optional, Dict

from utilities import create_logger, get_datetime, get_json_response
from data_collection.youtube_api._description_processing import get_description


def _save_response_to_tmp_file(tmp_filepath: str, response_dict: Dict, last_update_date: datetime) -> bool:
    """
    Save descriptions from page to tmp file

    :param tmp_filepath: path to temporary file
    :param response_dict: youtube page data as dictionary
    :param last_update_date: date to
    :return: True if descriptions data up to date
    """

    with open(tmp_filepath, 'a', newline='', encoding='utf-8') as file:
        for video_info in response_dict['items']:
            # End saving if video older than passed date
            if get_datetime(video_info['snippet']['publishedAt']) <= last_update_date:
                file.close()
                return True
            # Else save record to tmp file
            row = {'title': video_info['snippet']['title']}
            row.update(get_description(video_info['snippet']['description']))
            writer = csv.DictWriter(file, fieldnames=row.keys())
            writer.writerow(row)
    file.close()
    return False


def download_playlist(playlist_id: str, tmp_filepath: str, last_update_date_str: str = '') -> Optional[datetime]:
    """
    Save description from youtube API to tmp file up to given datetime and return latest video date

    :param playlist_id: playlist id from youtube
    :param tmp_filepath: path to temporary file
    :param last_update_date_str: datetime in format '%Y-%m-%dT%H:%M:%SZ'
    :return: Latest video date if successfully download, None if request failed
    """

    # Init
    log = create_logger('download_playlist')
    page_token = ''
    api_key = os.getenv('YOUTUBE_API')
    latest_video_date = get_datetime('')
    last_update_date = get_datetime(last_update_date_str)
    log.info(f'Trying to download all videos after {last_update_date} from playlist {playlist_id}')

    # Collect descriptions data until end of playlist or update to given date
    while True:
        # Get dict response from request
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10000&playlistId={playlist_id}&key={api_key}&pageToken={page_token}'
        if (response_dict := get_json_response(url)) is None:
            log.error(f'Failed downloading at page {page_token}, error occurred in handling {url} url request')
            return None

        # Check datetime of latest video
        if page_token == '':
            latest_video_date = get_datetime(response_dict['items'][0]['snippet']['publishedAt'])
            log.info('Found latest video date: {0}'.format(latest_video_date))

        # Save page to tmp file and check is playlist up to date
        if _save_response_to_tmp_file(tmp_filepath, response_dict, last_update_date):
            log.info(f'Playlist downloaded successfully up to given date {last_update_date}')
            return latest_video_date

        # End of playlist condition
        if 'nextPageToken' in response_dict:
            page_token = response_dict['nextPageToken']
        else:
            log.info('Playlist downloaded successfully')
            return latest_video_date
