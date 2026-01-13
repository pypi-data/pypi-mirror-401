from numbers import Real


def _validate_real(*values):
    """
    Internal helper to ensure all values are real numbers.
    """
    for v in values:
        if not isinstance(v, Real):
            raise TypeError(f"Expected a real number, got {type(v).__name__}")


def add(a, b):
    """
    Return the sum of two real numbers.
    """
    _validate_real(a, b)
    return a + b


def subtract(a, b):
    """
    Return the difference of two real numbers.
    """
    _validate_real(a, b)
    return a - b


def multiply(a, b):
    """
    Return the product of two real numbers.
    """
    _validate_real(a, b)
    return a * b


def divide(a, b):
    """
    Return the quotient of two real numbers.

    Raises:
        ZeroDivisionError: if b is zero
    """
    _validate_real(a, b)
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def power(a, b):
    """
    Return a raised to the power b.
    """
    _validate_real(a, b)
    return a ** b


def clamp(value, min_val, max_val):
    """
    Clamp a value between min_val and max_val.

    Raises:
        ValueError: if min_val > max_val
    """
    _validate_real(value, min_val, max_val)
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val")
    return max(min_val, min(value, max_val))
