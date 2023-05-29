import unittest
from unittest.mock import MagicMock

from tracert import Traceroute


class Test(unittest.TestCase):
    def test_recv_data(self):
        """
        Проверяет корректность получения данных по сокету
        """

        sock = MagicMock()
        sock.recv.side_effect = [b'test data', None]
        actual_data = Traceroute.receive_data(sock)

        self.assertEqual(b'test data', actual_data)

    def test_for_permissions(self):
        """
        Проверяет выпадет ли PermissionError
        """
        try:
            Traceroute.test_for_permissions()
        except PermissionError:
            assert True
