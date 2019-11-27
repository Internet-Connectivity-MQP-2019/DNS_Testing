import os
import sys
import unittest
from unittest import mock
from unittest.mock import patch, call
import geolocation
import geoip2.database


def expand_filename(filename):
    return os.path.join(os.path.dirname(__file__), filename)


class MockResponse(object):
    def __init__(self, d):
        for a, b in d.items():
           setattr(self, a, MockResponse(b) if isinstance(b, dict) else b)


# country, state, latitude, longitude, code
def mock_response(data):
    database_mock = mock.Mock()

    database_mock.city.side_effect = list([MockResponse({"country": {"name": d[0]},
                                                         "subdivisions": {"most_specific": {"name": d[1]}},
                                                         "location": {"latitude": d[2], "longitude": d[3]},
                                                         "postal": {"code": d[4]}}) for d in data])

    return database_mock


class MyTestCase(unittest.TestCase):

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_empty(self, mock_print, mock_geoip_reader):
        database_mock = mock.Mock()
        database_mock.configure({"city.return_value": {}})

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("empty.txt"))

        self.assertEqual(0, database_mock.city.call_count)

        self.assertEqual(0, mock_print.call_count)

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_oneIP_inUS_hasState(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("United States", "New Mexico", 42, -42, "42424")])
        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("one_ip.txt"))

        self.assertEqual(1, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42")])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("1.42.1.42,New Mexico,42,-42,42424")])

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_oneIP_inUS_noState(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("United States", None, 42, -42, None)])

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database2", expand_filename("one_ip.txt"))

        self.assertEqual(1, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42")])

        self.assertEqual(0, mock_print.call_count)

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database2")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_oneIP_outOfUS_noState(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("Canada", None, 42, -42, None)])

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("one_ip.txt"))

        self.assertEqual(1, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42")])

        self.assertEqual(0, mock_print.call_count)

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_oneIP_outOfUS_hasState(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("Canada", "Ontario", 42, -42, None)])

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("one_ip.txt"))

        self.assertEqual(1, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42")])

        self.assertEqual(0, mock_print.call_count)

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_multipleIPs_bothValid(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("United States", "Florida", 24, -42, "12345"),
                                       ("United States", "Vermont", 84, -24, "54321")])

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("two_ips.txt"))

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

        self.assertEqual(2, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42"), call("42.1.42.1")])

        self.assertEqual(2, mock_print.call_count)
        mock_print.assert_has_calls([call("1.42.1.42,Florida,24,-42,12345"),
                                     call("42.1.42.1,Vermont,84,-24,54321")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_multipleIPs_oneInvalid(self, mock_print, mock_geoip_reader):
        database_mock = mock_response([("United States", "Florida", 24, -42, "12345"),
                                       ("Canada", "Ontario", 84, -24, "54321")])

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("two_ips.txt"))

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

        self.assertEqual(2, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42"), call("42.1.42.1")])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("1.42.1.42,Florida,24,-42,12345")])

    @patch.object(geoip2.database, "Reader")
    @patch('builtins.print')
    def test_multipleIPs_exception(self, mock_print, mock_geoip_reader):
        database_mock = mock.Mock()
        database_mock.city.side_effect = [geoip2.errors.AddressNotFoundError(),
                                          MockResponse({"country": {"name": "United States"},
                                                        "subdivisions": {"most_specific": {"name": "Florida"}},
                                                        "location": {"latitude": 42, "longitude": 42},
                                                        "postal": {"code": "24680"}})]

        mock_geoip_reader.return_value = database_mock

        geolocation.geolocate_ips("test_database", expand_filename("two_ips.txt"))

        self.assertEqual(1, mock_geoip_reader.call_count)
        mock_geoip_reader.assert_has_calls([call("test_database")])

        self.assertEqual(2, database_mock.city.call_count)
        database_mock.city.assert_has_calls([call("1.42.1.42"), call("42.1.42.1")])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("42.1.42.1,Florida,42,42,24680")])

