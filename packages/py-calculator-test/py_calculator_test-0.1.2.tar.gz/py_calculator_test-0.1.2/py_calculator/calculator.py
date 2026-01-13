"""
calculator.py

This module provides a Calculator class to perform basic arithmetic operations
such as addition, subtraction, and multiplication.
"""

from typing import Union

Number = Union[int, float]

class Calculator :
    """Calculator class to perform Arithmetic operations"""

    def _validate(self, param01 : Number, param02 : Number) -> None:

        """ Validate the parameters either int or float """
        if not isinstance(param01, (int, float)) or not isinstance(param02, (int, float)) :
            raise TypeError("Both parameters must be numbers (int or float).")

    def addition(self, param01, param02) :
        """ Addition"""
        self._validate(param01, param02)
        return param01 + param02

    def subtraction(self, param01, param02) :
        """ Subtraction """
        self._validate(param01, param02)
        return param01 - param02

    def multiplication(self, param01, param02) :
        """ Multiplication """
        self._validate(param01, param02)
        return param01 * param02

    def division(self, param01, param02) :
        """ Division """
        self._validate(param01, param02)
        if param02 == 0 :
            raise ZeroDivisionError("Division by zero is not allowed.")
        return param01 / param02

    def modulus(self, param01, param02) :
        """ Returns the Modulus of two numbers"""
        self._validate(param01, param02)
        if param02 == 0 :
            raise ZeroDivisionError("Division by zero is not allowed.")
        return param01 % param02
