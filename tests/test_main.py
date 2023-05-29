import unittest

from main import main


class Test(unittest.TestCase):
    def test_main(self):
        """
        Тестирует функцию main
        """

        try:
            main()
        except Exception:
            assert False

        assert True

