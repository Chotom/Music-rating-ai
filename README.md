# Music-rating-ai
Machine learning project to forecast music rating by collected data

## Description
Albums rating are based on ratings from music reviewing channel: 
[theneedledrop](https://www.youtube.com/c/theneedledrop). All albums, used in
learning dataset, are available on Spotify and were collected 
through youtube and spotify api.

## Setup
1. run 
```shell
pip install -r requirements.txt
```

2. Set YOUTUBE_API env to your api key
3. Run tests to check setup
```shell
python -m unittest discover .
```

## CLI

Data collection CLI:
```shell
python ./data_collection/data_collecting_cli.py --help
```

## Tests

```shell
python -m unittest discover .
```
