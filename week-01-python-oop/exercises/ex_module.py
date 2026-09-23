# math_utils.py
PI = 3.14159

def area_circle(radius):
    return PI * radius ** 2

def area_square(side):
    return side ** 2


# greetings.py
DEFAULT_LANG = "en"

def hello(name):
    return f"Hello, {name}!"

def goodbye(name):
    return f"Goodbye, {name}!"


# stats.py
VERSION = "1.11"

def mean(numbers):
    return sum(numbers) / len(numbers)

def minimum(numbers):
    return min(numbers)

def maximum(numbers):
    return max(numbers)