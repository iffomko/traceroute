import sys

from tracert import Traceroute


def main():
    try:
        Traceroute().run(sys.argv[1])
    except PermissionError:
        print('\nНе хватает прав для запуска скрипта\n')

if __name__ == '__main__':
    main()
