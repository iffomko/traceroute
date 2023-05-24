import random
import struct


class IcmpPacket:
    ECHO_ANSWER = 0
    DESTINATION_UNREACHABLE = 3
    SOURCE_QUENCH = 4
    REDIRECT = 5
    ECHO_REQUEST = 8
    TTL_EXCEEDED = 11
    PARAMETER_PROBLEM_DATAGRAM = 12
    TIMESTAMP_REQUEST = 13
    TIMESTAMP_REPLAY = 14
    ADDRESS_MASK_REQUEST = 17
    ADDRESS_MASK_REPLAY = 18

    def __init__(self, icmp_type: int, icmp_code: int):
        self._icmp_type = icmp_type
        self._icmp_code = icmp_code

    def _get_checksum(self):
        icmp_temp = struct.pack('!2BH', self._icmp_type, self._icmp_code, 0)

        checksum = 0

        for i in range(0, len(icmp_temp), 2):
            checksum += (icmp_temp[i] << 8) + icmp_temp[i + 1]

        checksum = (checksum >> 16) + (checksum & 0xffff)

        return checksum & 0xffff

    def pack(self) -> bytes:
        return struct.pack('!2B3H', self._icmp_type, self._icmp_code, self._get_checksum(), 1, random.randint(400, 3000))
