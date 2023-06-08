import sys

from cli_parser import Parser
from enums.parser_enum import ParserEnum
from tracert import Traceroute


def main(argv: list):
    try:
        params = Parser().parse(argv)

        if params.get(ParserEnum.help_key):
            return params.get(ParserEnum.help_key_text)

        if params.get(ParserEnum.error):
            return params.get(ParserEnum.error_message)

        Traceroute(params).run()
    except PermissionError:
        return '\nНе хватает прав для запуска скрипта\n'


if __name__ == '__main__':
    print(main(sys.argv))
