import unittest

from year_of_bot import data, generate_fmt_dict


class TestData(unittest.TestCase):
    def test_data_is_all_valid(self):
        d = generate_fmt_dict()
        for g in data.predictions:
            for t in g:
                t.format(**d)
