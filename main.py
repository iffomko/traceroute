import sys

from tracert import Traceroute


def main():
    Traceroute().traceroute(sys.argv[1])


if __name__ == '__main__':
    main()
