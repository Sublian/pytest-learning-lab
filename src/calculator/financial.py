# financial.py
"""Módulo de operaciones financieras."""

import pandas as pd
import numpy as np
from typing import List

class FinancialCalculator:
    """Calculadora para operaciones financieras."""
    
    @staticmethod
    def compound_interest(principal: float, rate: float, time: int) -> float:
        """Calcula interés compuesto."""
        if principal < 0 or rate < 0 or time < 0:
            raise ValueError("Los valores no pueden ser negativos")
        return round(principal * (1 + rate) ** time, 2)
    
    @staticmethod
    def calculate_loan_payment(principal: float, annual_rate: float, years: int) -> float:
        """Calcula el pago mensual de un préstamo."""
        # if principal <= 0 or annual_rate <= 0 or years <= 0:
        #     raise ValueError("Todos los valores deben ser positivos")
        
        if principal <= 0:
            raise ValueError("El principal debe ser positivo")
        
        if years <= 0:
            raise ValueError("El plazo en años debe ser positivo")
        
        if annual_rate < 0:
            raise ValueError("La tasa de interés no puede ser negativa")
        
        monthly_rate = annual_rate / 12 / 100
        num_payments = years * 12
        
        if monthly_rate == 0:
            return round((principal / num_payments), 2)
        
        payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)
        return round(payment, 2)