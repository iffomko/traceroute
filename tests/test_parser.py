import unittest

from cli_parser import Parser
from enums.parser_enum import ParserEnum


class TestParser(unittest.TestCase):
    def test_help_command(self):
        expected_result = {
            ParserEnum.error: False,
            ParserEnum.help_key: True,
            ParserEnum.help_key_text: f'Справка:\r\n'
                                      f'{ParserEnum.trace_port_flag} - порт, на котором работает traceroute '
                                      f'(по-умолчанию стоит 80)\r\n'
                                      f'{ParserEnum.ttl_max_flag} - максимальное время жизни пакета '
                                      f'(максимальное количество прыжков по промежуточным узлам'
                                      f'по-умолчанию стоит 30)\r\n'
                                      f'{ParserEnum.timeout_flag} - максимальное время ожидания ответа'
                                      f'от промежуточного узла с фиксированным временем жизни (по-умолчанию'
                                      f'стоит 3 секунды)\r\n'
                                      f'{ParserEnum.target_flag} - адрес (ip или домен), маршрут которого'
                                      f'хотите получить (обязательный параметр)\r\n'
        }

        actual_result = Parser().parse(['--help'])

        self.assertDictEqual(expected_result, actual_result)

    def test_all_parser(self):
        expected_result = {
            ParserEnum.target_key: 'google.com',
            ParserEnum.timeout_key: 0.1,
            ParserEnum.ttl_max_key: 50,
            ParserEnum.trace_port_key: 81,
            ParserEnum.error: False
        }

        actual_result = Parser().parse('main.py --target google.com -t 0.1 --ttl-max 50 --trace-port 81'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_without_target_flag(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: 'Вы не указали адрес, маршрут которого хотите получить'
        }

        actual_result = Parser().parse('main.py -t 0.1 --ttl-max 50 --trace-port 81'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_with_incorrect_ttl_value(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: f'Вы не ввели не верное значение '
                                      f'для максимального времени жизни ({ParserEnum.ttl_max_flag})'
        }

        actual_result = Parser().parse('main.py -t 0.1 --ttl-max None --trace-port 81'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_with_incorrect_timeout_value(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: f'Вы не ввели не верное значение '
                                      f'для таймаута ожидания ({ParserEnum.timeout_flag})'
        }

        actual_result = Parser().parse('main.py -t None --ttl-max 30 --trace-port 81'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_only_with_target(self):
        expected_result = {
            ParserEnum.target_key: 'google.com',
            ParserEnum.timeout_key: 3,
            ParserEnum.ttl_max_key: 30,
            ParserEnum.trace_port_key: 80,
            ParserEnum.error: False
        }

        actual_result = Parser().parse('main.py --target google.com'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_not_find_element(self):
        expected_result = -1
        actual_result = Parser.find(['lol, kek, chebureck'], 'test')

        self.assertEqual(expected_result, actual_result)

    def test_only_without_value_target(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: 'Вы не указали адрес, маршрут которого хотите получить'
        }

        actual_result = Parser().parse('main.py --target'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_only_without_value_timeout(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: f'Вы не ввели не верное значение '
                                      f'для таймаута ожидания ({ParserEnum.timeout_flag})'
        }

        actual_result = Parser().parse('main.py --target google.com -t'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_only_without_value_ttl(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: f'Вы не ввели не верное значение '
                                      f'для максимального времени жизни ({ParserEnum.ttl_max_flag})'
        }

        actual_result = Parser().parse('main.py --target google.com --ttl-max'.split(' '))

        self.assertDictEqual(expected_result, actual_result)

    def test_only_without_value_trace_port(self):
        expected_result = {
            ParserEnum.error: True,
            ParserEnum.error_message: f'Вы не ввели порт, на котором будет '
                                      f'работать traceroute ({ParserEnum.trace_port_flag})'
        }

        actual_result = Parser().parse('main.py --target google.com --trace-port'.split(' '))

        self.assertDictEqual(expected_result, actual_result)
