"""
data.py - collection and dataset utilities for simptools

All functions work on lists or tuples of numbers.

"""

from math import sqrt
from numbers import Real

# -----------------------------
# Helper / validation functions
# -----------------------------

def _check_numbers(data):
    """Raise TypeError if data contains non-numbers."""
    for x in data:
        if not isinstance(x, Real):
            raise TypeError(f"All elements must be numbers, got {type(x).__name__}")


def _check_nonempty(data):
    """Raise ValueError if data is empty."""
    if not data:
        raise ValueError("Data cannot be empty")


# -----------------------------
# Statistics functions
# -----------------------------

def average(data):
    """Return the average (mean) of the numbers."""
    _check_nonempty(data)
    _check_numbers(data)
    return sum(data) / len(data)


def middle(data):
    """Return the middle value (median)."""
    _check_nonempty(data)
    _check_numbers(data)
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 1:
        return sorted_data[mid]
    else:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2


def spread(data):
    """Return the variance (average squared distance from mean)."""
    _check_nonempty(data)
    _check_numbers(data)
    avg = average(data)
    return sum((x - avg) ** 2 for x in data) / len(data)


def deviation(data):
    """Return the standard deviation (sqrt of variance)."""
    return sqrt(spread(data))


def normalize(data):
    """Scale numbers to range 0 → 1."""
    _check_nonempty(data)
    _check_numbers(data)
    min_val = min(data)
    max_val = max(data)
    if min_val == max_val:
        return [0.0 for _ in data]  # all numbers are the same
    return [(x - min_val) / (max_val - min_val) for x in data]


def zscore(data):
    """Return the z-scores of numbers (distance from mean in SD units)."""
    _check_nonempty(data)
    _check_numbers(data)
    sd = deviation(data)
    if sd == 0:
        return [0.0 for _ in data]  # all numbers identical
    avg = average(data)
    return [(x - avg) / sd for x in data]


# -----------------------------
# List / sequence helpers
# -----------------------------

def flatten(data):
    """Flatten a nested list/tuple."""
    result = []
    for item in data:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def split(data, size):
    """Split list into chunks of given size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [data[i:i+size] for i in range(0, len(data), size)]


def unique(data):
    """Return list with duplicates removed (preserve order)."""
    seen = set()
    result = []
    for x in data:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


def pairs(data):
    """Return consecutive value pairs."""
    return [(data[i], data[i+1]) for i in range(len(data)-1)]


def running(data):
    """Return cumulative sum of data."""
    _check_nonempty(data)
    _check_numbers(data)
    total = 0
    result = []
    for x in data:
        total += x
        result.append(total)
    return result


# -----------------------------
# Validation functions
# -----------------------------

def check(data):
    """Check that list is non-empty and contains only numbers."""
    _check_nonempty(data)
    _check_numbers(data)
    return True


def same(*data_lists):
    """Check that all provided lists have the same length."""
    if not data_lists:
        raise ValueError("No data provided")
    lengths = [len(lst) for lst in data_lists]
    if min(lengths) != max(lengths):
        raise ValueError("All lists must have the same length")
    return True


# -----------------------------
# Transformations
# -----------------------------

def scale(data, factor):
    """Multiply each number by a factor."""
    _check_nonempty(data)
    _check_numbers(data)
    return [x * factor for x in data]


def shift(data, value):
    """Add a value to each number."""
    _check_nonempty(data)
    _check_numbers(data)
    return [x + value for x in data]


def clip(data, low, high):
    """Clamp numbers to be between low and high."""
    _check_nonempty(data)
    _check_numbers(data)
    if low > high:
        raise ValueError("Low cannot be greater than high")
    return [max(low, min(x, high)) for x in data]
