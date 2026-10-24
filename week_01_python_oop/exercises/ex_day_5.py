# Exercise on 
# Error Handling
# Costome exeptions
# Defensive programing
'''
import json

# 1 exeptions
try:
    x = int("hello")
except ValueError as e:
    print(type(e).__name__)
    print(str(e)) 
 
print('='* 50)   
 
# 2 try/except - catching example

def safe_load_json(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print (f"File not found: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f'Json parse error: {e}')
        return {}
    finally:
        print ("load attempted")
        
if __name__ == '__main__':
    # 1. Missing file
    result = safe_load_json("nonexistent.json")
    print(f"Result: {result}")

    # 2. Malformed JSON
    with open("bad.json", "w") as f:
        f.write("{not valid json")
    result = safe_load_json("bad.json")
    print(f"Result: {result}")

    # 3. Valid JSON
    with open("good.json", "w") as f:
        f.write('{"name": "test", "value": 42}')
    result = safe_load_json("good.json")
    print(f"Result: {result}")'''

# 3 the exception hierarchy — why it matters
'''Write a function called parse_age(raw: str) -> int 
that converts a string to an age. 
Then write a function process_ages(ages: list[str]) -> list[int] 
that calls parse_age on each string.'''

def parse_age(raw: str) -> int:
    if raw.startswith('-') and raw[1:].isdigit():
        raise ValueError (f"age can not be negative: {raw!r}")
    if not raw.isdigit():
        raise ValueError (f"invalid age format: {raw!r}")
    age = int(raw)
    if age > 150:
        raise ValueError(f"you should be dead with {raw!r} of age")
    return age
def process_ages(ages: list[str]) -> list[int]:
    valid_ages = []
    for raw_age in ages:
        try:
            parse = parse_age(raw_age)
            valid_ages.append(parse)
        except ValueError as e:
            print (f"skipped entry {e}")
    
    return valid_ages
        
if __name__ == '__main__':
    raw_ages = ['25', 'abc', '42', '200', '0', '-3']
    valid_ages = process_ages(raw_ages)
    print(f'Valid ages: {valid_ages}')
    