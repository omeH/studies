import pytest

import correctness


class TestCorrectness(object):

    def setup_method(self, method):
        self.str_data_1 = '2014-10-08 09:34:17'
        self.str_data_2 = '1111-10-08 09:34:17'
        self.str_data_3 = '2014-13-08 09:34:17'
        self.str_data_4 = '2014-10-32 09:34:17'
        self.str_data_5 = '2014-10-08 25:34:17'
        self.str_data_6 = '2014-10-08 09:60:17'
        self.str_data_7 = '2014-10-08 09:34:60'
        self.str_data_8 = 'YYY4-M0-0D 0H:3M:S0'
        self.str_data_9 = '2014-10-08 09:34:1712'
        self.str_data_10 = '122014-10-08 09:34:17'

    def test_isdate(self):
        assert correctness.is_date_time(self.str_data_1) is True
        assert correctness.is_date_time(self.str_data_2) is False
        assert correctness.is_date_time(self.str_data_3) is False
        assert correctness.is_date_time(self.str_data_4) is False
        assert correctness.is_date_time(self.str_data_5) is False
        assert correctness.is_date_time(self.str_data_6) is False
        assert correctness.is_date_time(self.str_data_7) is False
        assert correctness.is_date_time(self.str_data_8) is False
        assert correctness.is_date_time(self.str_data_9) is False
        assert correctness.is_date_time(self.str_data_10) is False
