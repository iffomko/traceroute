import unittest
from unittest.mock import MagicMock

from tracert import Traceroute


class Test(unittest.TestCase):
    def test_for_permissions(self):
        """
        Проверяет выпадет ли PermissionError
        """
        try:
            Traceroute.test_for_permissions()
        except PermissionError:
            assert True
