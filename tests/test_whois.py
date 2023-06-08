import unittest
from unittest.mock import MagicMock

from whois import WhoisDataFinder


class Test(unittest.TestCase):
    test_whois = WhoisDataFinder()

    def test_def_data_is_none(self):
        """
        Тестирует правильность обработки значения None
        """

        self.assertEqual(self.test_whois._data_or_default(None), '')

    def test_def_data_is_not_none(self):
        """
        Тестирует правильность обработки значения, которое не является None
        """

        self.assertEqual(self.test_whois._data_or_default('123'), '123')

    def test_parse_whois_data_positive(self):
        """
        Тестирует правильность парсинга ответа от whois сервера (положительный случай)
        """
        actual_response = self.test_whois._parse_whois_response('whois:   www.google.com\norigin:     tele2.com\n')
        print(actual_response)
        expected_response = {'whois': 'www.google.com', 'origin': 'tele2.com'}
        print(expected_response)

        self.assertDictEqual(expected_response, actual_response)

    def test_parse_whois_data_negative(self):
        """
        Тестирует правильность парсинга ответа от whois сервера (негативный случай)
        """
        actual_response = self.test_whois._parse_whois_response('')
        expected_response = {}

        self.assertEqual(expected_response, actual_response)

    def test_white_ip(self):
        """
        Тестирует правильность работы проверки на "белоту" ip (положительный случай)
        """

        self.assertTrue(self.test_whois.is_white_ip('234.10.34.1'))

    def test_not_white_ip(self):
        """
        Тестирует правильность работы проверки на "белоту" ip (негативный случай)
        """

        self.assertFalse(self.test_whois.is_white_ip('192.168.34.1'))

    def test_is_local(self):
        """
        Проверяет случай когда ip серый
        """

        self.assertEqual(
            {'local': True, 'local_text': self.test_whois._LOCAL_TEXT},
            self.test_whois.get_data_from_whois_server('192.168.34.1')
        )

    def test_recv_data(self):
        """
        Проверяет корректность получения данных по сокету
        """

        sock = MagicMock()
        sock.recv.side_effect = [b'test data', None]
        actual_data = self.test_whois.receive_data(sock)

        self.assertEqual(b'test data', actual_data)
