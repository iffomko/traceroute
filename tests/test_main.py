import unittest

from enums.parser_enum import ParserEnum
from main import main


class Test(unittest.TestCase):
    def test_start_main(self):
        """
        Тестирует функцию main
        """

        main([])

        assert True

    def test_print_help_command(self):
        actual_result = main([ParserEnum.help_flag])
        expected_result = f'Справка:\r\n' \
                          f'{ParserEnum.trace_port_flag} - порт, на котором работает traceroute ' \
                          f'(по-умолчанию стоит 80)\r\n' \
                          f'{ParserEnum.ttl_max_flag} - максимальное время жизни пакета ' \
                          f'(максимальное количество прыжков по промежуточным узлам' \
                          f'по-умолчанию стоит 30)\r\n' \
                          f'{ParserEnum.timeout_flag} - максимальное время ожидания ответа' \
                          f'от промежуточного узла с фиксированным временем жизни (по-умолчанию' \
                          f'стоит 3 секунды)\r\n' \
                          f'{ParserEnum.target_flag} - адрес (ip или домен), маршрут которого' \
                          f'хотите получить (обязательный параметр)\r\n'

        self.assertEqual(expected_result, actual_result)

    def test_with_exception(self):
        actual_result = main('main.py --target google.com --ttl-max'.split(' '))
        expected_result = f'Вы не ввели не верное значение ' \
                          f'для максимального времени жизни ({ParserEnum.ttl_max_flag})'

        self.assertEqual(expected_result, actual_result)

    def test_run_traceroute(self):
        actual_result = main('main.py --target google.com'.split(' '))
        expected_result = '\nНе хватает прав для запуска скрипта\n'

        self.assertEqual(expected_result, actual_result)
