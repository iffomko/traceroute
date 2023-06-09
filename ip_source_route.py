import socket
import struct


class IPSourceRoute:
    TYPE_STRICT_SOURCE_ROUTE = 137
    TYPE_LOOSE_SOURCE_ROUTE = 131

    def __init__(self, TYPE: int, DATA: list):
        self._TYPE = TYPE
        self._DATA = DATA

    @staticmethod
    def length(data: list) -> int:
        return len(data) * 4 + 3

    def pack(self):
        ips = b''

        for ip in self._DATA:
            ips += socket.inet_aton(ip)

        return struct.pack(
            '!3B',
            self._TYPE,
            self.length(self._DATA),
            4
        ) + ips
