Concept 1: what a class actually is

You already think in objects. A dataset has columns, shape, dtypes, and methods like .describe(). A Scikit-learn model has parameters and a .fit() method. You've been using objects constantly — today you learn to build them from scratch.

A class is a blueprint. An object is what you build from that blueprint. The blueprint for a house describes rooms, walls, and doors. Each actual house built from it is a separate object — same structure, different contents.

In Python, a class packages two things together: data (called attributes) and behavior (called methods). Once you define the blueprint, you can stamp out as many objects as you need, each with its own independent data.

class DatabaseProfile:
  def __init__(self, name, row, column):
    self.name = name
    self.row = row
    self.column = column
  def summary(self):
    return f"{self.name}: {self.row} row * {self.column}column"  
  def is_large(self):
    return self.row > 100000

sales = DatabaseProfile("Sales_q4", 25000, 18) 
customers = DatabaseProfile("Customer", 42000, 9)

print(sales.summary())  # Output: Sales_q4: 25000 row * 18column
print(sales.is_large()) # Output: False
print(customers.summary())  # Output: Customer: 42000 row * 9column
print(customers.is_large()) # Output: False

__init__ runs automatically the moment you call DatabaseProfile(...). 
It's the constructor. self is just the object referring to itself — every instance method receives it as the first argument. 
When you call sales.summary(), Python silently translates that to DatabaseProfile.summary(sales).