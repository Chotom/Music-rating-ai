import re
from typing import Dict

_REGEX_PATTERNS = [
    r'(.*) - (.*) / ((19|20|21)[0-9][0-9]) / (.*) / (.*)',  # author - album / year / label / genres
    r'(.*) - (.*) / (.*) / ((19|20|21)[0-9][0-9]) / (.*)',  # author - album / label / year / genres
    r'(.*)- (.*) / ((19|20|21)[0-9][0-9]) / (.*) / (.*)',  # author- album / year / label / genres
    r'(.*)- (.*) / (.*) / ((19|20|21)[0-9][0-9]) / (.*)',  # author- album / label / year / genres
    r'(.*) - (.*) - ((19|20|21)[0-9][0-9]) / (.*) / (.*)',  # author - album - year / label / genres
    r'(.*) - (.*) - (.*)/ ((19|20|21)[0-9][0-9]) / (.*)',  # author - album - label / year / genres
    r'(.*)- (.*) / ((19|20|21)[0-9][0-9]) / (.*)',  # author - album / year / genres
    r'(.*) (.*) / (.*) / (.*) / (.*)',  # VARIOUS ARTISTS / label / name / genres
    r'(.*) (.*) / ((19|20|21)[0-9][0-9]) / (.*)',  # VARIOUS ARTISTS / year / genres
]


def get_description(description: str) -> Dict:
    """
    Find album specification from given string and save it to dictionary.
    Function search for author, album name, rating, year of production and genres.

    :param description: review description with album specification
    :return: dict with {'author', 'album', 'rate', 'year', 'genre'} keys
    """

    # Init
    description_dict = {'author': None, 'album': None, 'rate': None, 'year': None, 'genres': None}

    # Save sentences from description rows without empty lines in an array
    description_rows_array = [row for row in description.split('\n') if row != '']

    # Search values in description
    for row in description_rows_array:
        # Find author, album, year, genres by defined pattern
        for i, pattern in enumerate(_REGEX_PATTERNS):
            if (artist_regex := re.search(pattern, row)) is not None:
                description_dict['author'] = artist_regex.group(1).lower()
                description_dict['album'] = artist_regex.group(2).lower()
                description_dict['year'] = artist_regex.group((i % 2) + 3).lower()
                description_dict['genres'] = artist_regex.groups()[-1].lower().split(',')
                break
        # Find rating
        rate_regex = re.search(r'(.*)/10', row)
        if rate_regex is not None and 'listen' not in rate_regex.group(0).split('/')[0].lower():
            description_dict['rate'] = rate_regex.group(0).split('/')[0].lower()

    return description_dict
