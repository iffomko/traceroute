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

    @staticmethod
    def from_bytes(packet: bytes) -> 'IcmpPacket':
        packet_tuple = struct.unpack('!2B', packet[:2])

        return IcmpPacket(packet_tuple[0], packet_tuple[1])

    def _get_checksum(self):
        packet_temp = struct.pack('!2BH', self._icmp_type, self._icmp_code, 0)

        acc = 0

        for i in range(0, len(packet_temp), 2):
            acc += (packet_temp[i] << 8) + packet_temp[i + 1]

        checksum = (acc >> 16) + (acc & 0xffff)

        return checksum & 0xffff

    def pack(self) -> bytes:
        return struct.pack(
            '!2B3H', self._icmp_type, self._icmp_code, self._get_checksum(), 1, random.randint(256, 3000)
        )
