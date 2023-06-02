import sys

from cli_parser import Parser
from enums.parser_enum import ParserEnum
from tracert import Traceroute


def main():
    try:
        params = Parser().parse(sys.argv)

        if params.get(ParserEnum.help_key):
            print(params.get(ParserEnum.help_key_text))
            return

        if params.get(ParserEnum.error):
            print(params.get(ParserEnum.error_message))
            return

        Traceroute(params).run()
    except PermissionError:
        print('\nНе хватает прав для запуска скрипта\n')


if __name__ == '__main__':
    main()
