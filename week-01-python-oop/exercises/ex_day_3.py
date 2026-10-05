import ex_module

print(ex_module.PI)
print(ex_module.area_circle(2))

from ex_module import area_circle, PI

print(area_circle(2))                   # 12.56636
print(PI)                               # 3.14159

# main.py
from ex_module import hello, goodbye, DEFAULT_LANG

print(hello("Alice"))                   # Hello, Alice!
print(goodbye("Bob"))                   # Goodbye, Bob!
print(DEFAULT_LANG)                     # en

ex_module 

print(f"Version: {ex_module .VERSION}")
print(f"Mean: {ex_module .mean([1, 2, 3, 4, 5])}")
print(f"Minimum: {ex_module .minimum([4, 2, 9, 1])}")
print(f"Maximum: {ex_module .maximum([4, 2, 9, 1])}")

import sys
print('ex_module' in sys.modules)

import sys
print('dataset' in sys.modules)