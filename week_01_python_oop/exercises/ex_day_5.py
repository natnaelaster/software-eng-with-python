# Exercise on 
# Error Handling
# Costome exeptions
# Defensive programing

import json

#exeptions
# 1
try:
    x = int("hello")
except ValueError as e:
    print(type(e).__name__)
    print(str(e)) 
 
print('='* 50)   
 
# 2
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
    print(f"Result: {result}")
