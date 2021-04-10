# Sample unit test
import unittest
from data_collection.youtube_api._description_processing import get_description


class TestBasicDescriptionCases(unittest.TestCase):
    def setUp(self):
        self.desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
                    "\n" \
                    "The songwriting and vocal performances on some album often leave a lot to be desired, though the " \
                    "random production is pretty stellar.\n" \
                    "===================================\n" \
                    "\n" \
                    "\n" \
                    "SOME ARTIST - some album / 2020 / YEAR0001 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
                    "\n" \
                    "5/10\n" \
                    "\n" \
                    "Y'all know this is just my opinion, right?"

    def test_normal_author(self):
        result = get_description(self.desc)
        self.assertEqual('some artist', result['author'])

    def test_normal_album(self):
        result = get_description(self.desc)
        self.assertEqual('some album', result['album'])

    def test_normal_year(self):
        result = get_description(self.desc)
        self.assertEqual('2020', result['year'])

    def test_normal_genres(self):
        result = get_description(self.desc)
        self.assertEqual(['cloud rap', ' ambient pop', ' alternative r&b'], result['genres'])


class TestVariousRatingCases(unittest.TestCase):
    def test_normal_rating(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "The songwriting and vocal performances on some album often leave a lot to be desired, though the random production is pretty stellar.\n" \
               "\n" \
               "More rap reviews: https://www.youtube.com/playlist?list...\n" \
               "\n" \
               "===================================\n" \
               "FAV TRACKS: MY AGENDA, YAYO, BOYLIFE IN EU, VIOLENCE, HELLRAISER, ICEHEART\n" \
               "\n" \
               "LEAST FAV TRACK: BUTTERFLY PARALYZED\n" \
               "\n" \
               "SOME ARTIST - some album / 2020 / YEAR0001 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "5/10\n" \
               "\n" \
               "Y'all know this is just my opinion, right?"

        result = get_description(desc)
        self.assertEqual('5', result['rate'])

    def test_not_good_rating(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "The songwriting and vocal performances on some album often leave a lot to be desired, though the random production is pretty stellar.\n" \
               "\n" \
               "More rap reviews: https://www.youtube.com/playlist?list...\n" \
               "\n" \
               "SOME ARTIST - some album / 2020 / YEAR0001 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "NOT GOOD/10"

        result = get_description(desc)
        self.assertEqual('not good', result['rate'])

    def test_none_rating(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "The songwriting and vocal performances on some album often leave a lot to be desired, though the random production is pretty stellar.\n" \
               "\n" \
               "More rap reviews: https://www.youtube.com/playlist?list...\n" \
               "\n" \
               "\n" \
               "SOME ARTIST - some album / 2020 / YEAR0001 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "5/asdasd"

        result = get_description(desc)
        self.assertIsNone(result['rate'])


class TestVariousRegexCombination(unittest.TestCase):
    def test_label_first_rating(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "SOME ARTIST - some album / YEAR0001 / 2020 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "5/10"

        result = get_description(desc)
        self.assertEqual('2020', result['year'])
        self.assertEqual('some artist', result['author'])
        self.assertEqual('some album', result['album'])
        self.assertEqual(['cloud rap', ' ambient pop', ' alternative r&b'], result['genres'])

    def test_no_artist_found(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "" \
               " 2020 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "5/10"

        result = get_description(desc)
        self.assertIsNone(result['author'])
        self.assertIsNone(result['album'])

    def test_various_artists_found(self):
        desc = "Listen: https://www.youtube.com/watch?v=vYdmr...\n" \
               "\n" \
               "" \
               "VARIOUS ARTISTS / YEAR0001 / 2020 / CLOUD RAP, AMBIENT POP, ALTERNATIVE R&B\n" \
               "\n" \
               "5/10"

        result = get_description(desc)
        self.assertEqual('various', result['author'])
        self.assertEqual('artists', result['album'])
