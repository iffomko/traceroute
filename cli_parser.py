from enums.parser_enum import ParserEnum


class Parser:
    def __init__(self):
        self._STANDARD_PORT = 80
        self._STANDARD_MAX_TTL = 30
        self._STANDARD_TIMEOUT = 3

    @staticmethod
    def find(array: list, target: str) -> int:
        for i in range(len(array)):
            if array[i] == target:
                return i

        return -1

    def parse(self, argv: list) -> dict:
        if ParserEnum.help_flag in argv:
            return {
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

        params = dict()

        if ParserEnum.trace_port_flag in argv:
            try:
                params[ParserEnum.trace_port_key] = int(argv[self.find(argv, ParserEnum.trace_port_flag) + 1])
            except IndexError:
                pass
        else:
            params[ParserEnum.trace_port_key] = self._STANDARD_PORT

        if ParserEnum.ttl_max_flag in argv:
            try:
                params[ParserEnum.ttl_max_key] = int(argv[self.find(argv, ParserEnum.ttl_max_flag) + 1])
            except IndexError:
                pass
            except ValueError:
                return {
                    ParserEnum.error: True,
                    ParserEnum.error_message: f'Вы не ввели не верное значение '
                                              f'для максимального времени жизни ({ParserEnum.ttl_max_flag})'
                }
        else:
            params[ParserEnum.ttl_max_key] = self._STANDARD_MAX_TTL

        if ParserEnum.timeout_flag in argv:
            try:
                params[ParserEnum.timeout_key] = int(argv[self.find(argv, ParserEnum.timeout_flag) + 1])
            except IndexError:
                pass
            except ValueError:
                params[ParserEnum.timeout_key] = float(argv[self.find(argv, ParserEnum.timeout_flag) + 1])
        else:
            params[ParserEnum.timeout_key] = self._STANDARD_TIMEOUT

        if ParserEnum.target_flag in argv:
            try:
                params[ParserEnum.target_key] = argv[self.find(argv, ParserEnum.target_flag) + 1]
            except IndexError:
                pass
        else:
            return {
                ParserEnum.error: True,
                ParserEnum.error_message: 'Вы не указали адрес, маршрут которого хотите получить'
            }

        params[ParserEnum.error] = False

        return params
