import unittest

from trace_view import TraceView


class Test(unittest.TestCase):
    test_view = TraceView()

    def test_print_number_test_equals_numbers(self):
        """
        Тестирование получение нормализованного формата для номера строчки,
        если количество цифр в максимальном количестве номеров равна текущему номеру
        """
        actual_result = self.test_view._format_number_trace('1', 9)
        expected_result = '1.'

        assert actual_result == expected_result
        self.assertEqual(expected_result, actual_result)

    def test_print_number_test_different_numbers(self):
        """
        Тестирование получение нормализованного формата для номера строчки,
        если количество цифр в максимальном количестве номеров отличается от текущего номера
        """
        actual_result = self.test_view._format_number_trace('1', 10)
        expected_result = '1. '

        self.assertEqual(expected_result, actual_result)

    def test_getting_header(self):
        """
        Получение заголовка для начала тресировки
        """

        actual_result = self.test_view.get_header('ya.ru', '10.20.30.40', 30)
        expected_result = f'Трассировка маршрута к ya.ru [10.20.30.40]\n' \
                          f'с максимальным числом прыжков 30:\n'

        self.assertEqual(expected_result, actual_result)

    def test_generate_spaces_if_diff(self):
        """
        Проверяет правильность создания пробелов если значения разные по длине
        """

        actual_result = self.test_view._generate_spaces('123', '1')
        expected_result = '  '

        self.assertEqual(expected_result, actual_result)

    def test_generate_spaces_if_eq(self):
        """
        Проверяет правильность создания пробелов если значения одинаковые по длине
        """

        actual_result = self.test_view._generate_spaces('123', '542')
        expected_result = ''

        self.assertEqual(expected_result, actual_result)

    def test_for_def_if_none(self):
        """
        Проверяет, будет ли возвращена пустая строчка
        """

        actual_result = self.test_view._data_or_default(None)
        expected_result = ''

        self.assertEqual(expected_result, actual_result)

    def test_for_def_if_not_none(self):
        """
        Проверяет, будет ли возвращены данные
        """

        actual_result = self.test_view._data_or_default('test data')
        expected_result = 'test data'

        self.assertEqual(expected_result, actual_result)

    def test_for_def_if_none_and_default_other(self):
        """
        Проверяет, будет ли возвращена стандартное значение
        """

        actual_result = self.test_view._data_or_default(None, 'Нет данных')
        expected_result = 'Нет данных'

        self.assertEqual(expected_result, actual_result)

    def test_for_def_if_not_none_and_default_other(self):
        """
        Проверяет, будет ли возвращены данные
        """

        actual_result = self.test_view._data_or_default('test data', 'нет данных')
        expected_result = 'test data'

        self.assertEqual(expected_result, actual_result)

    def test_view_trace_if_not_fin(self):
        """
        Проверяет выведется результат звездочка, если мы не нашли ip
        """

        actual_result = self.test_view.get_view_trace(False, '', {'local': False}, 1, 30)
        expected_result = f'1.  *\r\n'

        self.assertEqual(expected_result, actual_result)

    def test_view_trace_if_fin(self):
        """
        Проверяет выведется результат звездочка, если мы нашли ip
        """

        actual_result = self.test_view.get_view_trace(True, '10.20.30.40', {'local': False}, 1, 30)
        expected_result = f'1.  10.20.30.40 \r\n'

        self.assertEqual(expected_result, actual_result)
