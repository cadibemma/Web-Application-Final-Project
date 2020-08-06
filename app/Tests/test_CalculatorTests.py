import unittest

from app.Calculator.Calculator import Calculator


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.calculator = Calculator()

    def test_results_property_calculator(self):
        self.assertEqual(self.calculator.result, 0)

    def test_add_method_calculator(self):
        self.assertEqual(self.calculator.add(2, 2), 4)
        self.assertEqual(self.calculator.result, 4)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.add(row['Value 2'], row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_subtract_method_calculator(self):
        self.assertEqual(self.calculator.subtract(2, 2), 0)
        self.assertEqual(self.calculator.result, 0)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.subtract(row['Value 2'], row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_multiply_method_calculator(self):
        self.assertEqual(self.calculator.multiply(2, 2), 4)
        self.assertEqual(self.calculator.result, 4)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.multiply(row['Value 2'], row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_divide_method_calculator(self):
        self.assertEqual(self.calculator.divide(2, 2), 1)
        self.assertEqual(self.calculator.result, 1)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.divide(row['Value 2'], row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_square_method_calculator(self):
        self.assertEqual(self.calculator.square(2), 4)
        self.assertEqual(self.calculator.result, 4)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.square(row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_square_root_method_calculator(self):
        self.assertEqual(self.calculator.squareroot(4), 2)
        self.assertEqual(self.calculator.result, 2)
        test_data = CsvReader().data
        for row in test_data:
            result = float(row['Result'])
            self.assertEqual(self.calculator.squareroot(row['Value 1']), result)
            self.assertEqual(self.calculator.result, result)

    def test_instantiate_calculator(self):
        self.assertIsInstance(self.calculator, Calculator)


if __name__ == '__main__':
    unittest.main()