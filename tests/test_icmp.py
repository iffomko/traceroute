import unittest

from icmp import IcmpPacket


class Test(unittest.TestCase):
    def test_icmp_pack(self):
        """
        Тестирует правильность создания icmp пакета
        """
        actual_result = IcmpPacket(8, 0).pack()
        expected_result = b'\x08\x00\x08\x00\x00\x01\x01\x00'

        self.assertEqual(expected_result, actual_result)

    def test_icmp_unpack(self):
        """
        Тестирует распаковку icmp пакета
        """
        actual_result = IcmpPacket.from_bytes(b'\x08\x00\x08\x00\x00\x01\x01\x00')

        assert actual_result._icmp_type == 8 and actual_result._icmp_code == 0
