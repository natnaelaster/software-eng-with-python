# Python & CS Journey — 10 Weeks to AI Agent Developer

> From Data Analyst to AI Agent Builder
> Started: [15-09-2026]
> Target: [30-03-2027]

## Why I'm Doing This
I am a data analyst with 2+ years of experience transitioning into AI agent development. This repository documents every concept I learn, every problem I solve, and every project I build along the way.

## Progress Tracker

| Week | Topic | Status | Score | Project |
|------|-------|--------|-------|---------|
| 1 | Python OOP & Programming | ✅ Complete | 91% | [Link] |
| 2 | Data Structures | 🔄 In Progress | - | - |
| 3 | Algorithms | ⏳ Upcoming | - | - |
| 4 | Software Engineering | ⏳ Upcoming | - | - |
| 5 | AI/ML Deep | ⏳ Upcoming | - | - |
| 6 | LLMs & Prompting | ⏳ Upcoming | - | - |
| 7 | RAG & Memory | ⏳ Upcoming | - | - |
| 8 | AI Agents | ⏳ Upcoming | - | - |
| 9 | User Interfaces | ⏳ Upcoming | - | - |
| 10 | Deployment + Final | ⏳ Upcoming | - | - |

## Skills Gained So Far
(update weekly)
- [✅] OOP and class design
- [ ] Data structures from scratch
- [ ] Algorithm analysis
- [ ] FastAPI backend development
- [ ] RAG systems
- [ ] AI agent building
- [ ] Streamlit UI
- [ ] Docker and deployment

## Projects Built
(link each one as you build it)
1. [Final AI Agent](link) — Week 10
2. [RAG System](link) — Week 7
3. [FastAPI Backend](link) — Week 4

## Weekly Notes

### Week 1 — Python OOP

#### Classes and objects

- A `class` is a blueprint, and an `object` is one instance with its own data. `self` is just the first parameter that receives the instance.
- `Instance attributes` are per-object, and class `attributes` are shared. Assigning to an instance creates a shadowing instance attribute and never changes the class one.
- `@classmethod` receives cls and is used for alternative constructors. `@staticmethod` receives neither.
- `@property` lets you run validation or computation behind plain attribute syntax. No setter means read-only.
- `__repr__` is for developers (and should reconstruct the object). `__str__` is for print.

####  Inheritance and dunders

- A child inherits everything and overrides what differs. `super().method()` calls the next class up the MRO, and not “the parent” by name.
- Polymorphism means calling the same method name on different types and getting type-specific behavior with no type checks.
- `isinstance` includes subclasses. type(x) is C does not.
- Each dunder unlocks one protocol:` __len__ →` len(), `__contains__` → in, `__iter__` → loops, `__getitem__` → [], `__lt__` → sorting, `__add__` → + (returns a new object).
- Defining `__eq__` without `__hash__` makes your object unhashable, because equal objects must hash equally.

#### Modules and packages

- A module is a namespace created by executing a `.py` file once. Python caches it in `sys.modules`.
- A package is a folder with `__init__.py`, and that file defines the package’s `public API`.
- A leading dot (`from .column import X`) means a relative import, resolved inside the current package.
- `if __name__ == "__main__"`: runs only when the file is executed directly, never on import.
- A virtual environment isolates dependencies per project. Commit `requirements.txt`, never `.venv/` or `.env`.

#### File I/O

- with guarantees `__exit__` runs even on exceptions. Build your own with `__enter__/__exit__`.
- Iterate files line by line. `f.read()` loads everything into RAM.
- `dumps`/`loads` work on strings, and `dump`/`load` work on file objects. `numpy` types need a custom `JSONEncoder`.
- CSV needs `newline=""`. `DictReader` and `DictWriter` use column names instead of indexes.
- `pathlib.Path` joins with `/`, and `mkdir(parents=True, exist_ok=True)` is safe to repeat.

#### Exceptions

- Python checks `except` clauses top to bottom and runs the first match, so put specific exceptions before general ones.
- `else` runs only if nothing was raised. `finally` always runs.
- A bare raise inside `except` re-raises with the original traceback. `except Exception: pass` hides bugs.
- Catching a parent class catches all its children, which is why you build hierarchies.
- Custom exceptions carry data as attributes. Call `super().__init__(message)` so `str(e)` works.

#### Decorators, generators, comprehensions

`@d` means `f = d(f)`, and the decorator runs at definition time. Always use` @wraps` and `return result`.
A decorator with arguments has three layers, because `@retry(3)` must return the actual decorator.
A generator function returns a generator object without running its body, and it can be consumed only once.
A list comprehension is `O(n)` memory. A `generator` expression is `O(1)`.
`key= `takes a function. `map` and `filter` return lazy iterators.

### Week 2 — Data structures from scratch with Python 

...

Daily Git Workflow

Follow this every single day:

bash
# Morning — start your day
git pull origin main

# While working — commit often
git add .
git commit -m "Day 12: implement BST insert and delete"

# End of day — always push
git push origin main

Commit message format to follow:

Day [number]: [what you built or learned]

Examples:
Day 1:  implement Stack class with push/pop/peek
Day 8:  solve linked list reversal problem
Day 15: complete Week 2 summary quiz (87%)
Day 23: build FastAPI route for agent endpoint


