import unittest
from solution import strict

class TestStrictDecorator(unittest.TestCase):
    def test_correct_types(self):
        """Проверка функции с правильными типами аргументов"""
        @strict
        def add(a: int, b: int) -> int:
            return a + b
        
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-1, 1), 0)
    
    def test_incorrect_type_first_arg(self):
        """Проверка функции с неправильным типом первого аргумента"""
        @strict
        def multiply(a: int, b: float) -> float:
            return a * b
        
        with self.assertRaises(TypeError) as context:
            multiply("2", 3.5)
        self.assertIn("Argument 'a' must be of type int, got str", str(context.exception))
    
    def test_incorrect_type_second_arg(self):
        """Проверка функции с неправильным типом второго аргумента"""
        @strict
        def concatenate(a: str, b: str) -> str:
            return a + b
        
        with self.assertRaises(TypeError) as context:
            concatenate("Hello, ", 123)
        self.assertIn("Argument 'b' must be of type str, got int", str(context.exception))
    
    def test_multiple_incorrect_types(self):
        """Проверка функции с несколькими неправильными типами аргументов"""
        @strict
        def process(a: bool, b: float, c: str) -> None:
            pass
        
        with self.assertRaises(TypeError) as context:
            process("True", "3.14", 100)
        # Проверяем, что ошибка касается первого неправильного аргумента
        self.assertIn("Argument 'a' must be of type bool, got str", str(context.exception))
    
    def test_no_annotations(self):
        """Проверка функции без аннотаций типов (декоратор ничего не делает)"""
        @strict
        def greet(a, b):
            return f"{a} {b}"
        
        self.assertEqual(greet("Hello", 123), "Hello 123")
        self.assertEqual(greet(1, 2), "1 2")
    
    def test_partial_annotations(self):
        """Проверка функции с частичными аннотациями типов"""
        @strict
        def func(a: int, b, c: str) -> None:
            pass
        
        # Проверяем только аргументы с аннотациями
        func(10, "anything", "test")  # Должно пройти без ошибок
        with self.assertRaises(TypeError) as context:
            func("10", "anything", "test")
        self.assertIn("Argument 'a' must be of type int, got str", str(context.exception))
        
        with self.assertRaises(TypeError) as context:
            func(10, "anything", 123)
        self.assertIn("Argument 'c' must be of type str, got int", str(context.exception))

if __name__ == '__main__':
    unittest.main()
