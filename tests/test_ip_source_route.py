import socket
import struct
import unittest

from ip_source_route import IPSourceRoute


class TestSourceRoute(unittest.TestCase):
    def test_loose_source_route(self):
        ips = ['10.20.30.40']
        ips_bytes = b''

        for ip in ips:
            ips_bytes += socket.inet_aton(ip)

        expected_result = struct.pack(
            '!3B',
            IPSourceRoute.TYPE_LOOSE_SOURCE_ROUTE,
            len(ips) * 4 + 3,
            4
        ) + ips_bytes

        self.assertEqual(expected_result, IPSourceRoute(IPSourceRoute.TYPE_LOOSE_SOURCE_ROUTE, ips).pack())

    def test_strict_source_route(self):
        ips = ['10.20.30.40']
        ips_bytes = b''

        for ip in ips:
            ips_bytes += socket.inet_aton(ip)

        expected_result = struct.pack(
            '!3B',
            IPSourceRoute.TYPE_STRICT_SOURCE_ROUTE,
            len(ips) * 4 + 3,
            4
        ) + ips_bytes

        self.assertEqual(expected_result, IPSourceRoute(IPSourceRoute.TYPE_STRICT_SOURCE_ROUTE, ips).pack())
