"""Módulo de operaciones matemáticas básicas."""

class MathOperations:
    """Clase para operaciones matemáticas."""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Suma dos números."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Los argumentos deben ser números")
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Resta dos números."""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiplica dos números."""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide dos números."""
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Calcula la potencia de un número."""
        return base ** exponent
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calcula el factorial de un número."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("El número debe ser un entero no negativo")
        if n == 0:
            return 1
        return n * MathOperations.factorial(n - 1)