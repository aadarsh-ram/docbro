"""
docbrostart

:name: Arithmetic New Operations
:description: This module contains functions for arithmetic operations

docbroend
"""

def add_two_nos(a, b):
    """
    docbrostart

    :name: add_two_nos
    :description: Adds two numbers
    :param a: This is the first number
    :param b: This is the second number
    :returns: The addition of first and second number
    :raises TypeError: The arguments must be numbers
    :markdown_start:

    ## This is a cool module
    ### Really cool!
    ```python
    print('Hello World')
    ```
    [This is a link](www.google.com)
    :markdown_end:

    docbroend
    """
    try:
        return a+b
    except TypeError:
        raise TypeError('The arguments must be numbers')

def sub_two_nos(a, b):
    """
    docbrostart

    :name: sub_two_nos
    :description: Subtracts two numbers
    :param a: This is the first number
    :param b: This is the second number
    :returns: The subtraction of first and second number
    :raises TypeError: The arguments must be numbers

    docbroend
    """
    try:
        return a-b
    except TypeError:
        raise TypeError('The arguments must be numbers')

def mul_two_nos(a, b):
    """
    docbrostart

    :name: mul_two_nos
    :description: Multiplies two numbers
    :param a: This is the first number
    :param b: This is the second number
    :returns: The multiplication of first and second number
    :raises TypeError: The arguments must be numbers

    docbroend
    """
    try:
        return a*b
    except:
        raise TypeError('The arguments must be numbers')

def div_two_nos(a, b):
    """
    docbrostart

    :name: div_two_nos
    :description: Divides two numbers
    :param a: This is the first number
    :param b: This is the second number
    :returns: The division of first and second number
    :raises TypeError: The arguments must be numbers

    docbroend
    """
    try:
        return a/b
    except:
        raise TypeError('The arguments must be numbers')