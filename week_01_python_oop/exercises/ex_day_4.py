# Exercise on 
# Context Manager- The Real Reasson for (with)

class Timer:
    def __init__(self, label):
        self.label = label
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        elapsed_time = self.end_time - self.start_time
        print(f"[{self.label}] elapsed time:{elapsed_time:.6f} sec")
        return False

if __name__ == "__main__":
    import time
    with Timer('loop test'):
        total = 0
        for i in range(1_000_000):
            total += 1    
            
    print('done')        


import os
import tempfile
import shutil

class TempDir:
    def __init__(self, prefix="tmp"):
        self.prefix = prefix
        self.path = None
        
    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix=self.prefix)  
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path is not None:
            shutil.rmtree(self.path)
        return False
    
if __name__ == "__main__":
    with TempDir(prefix="mytest_") as path:
        print(f"Created: {path}")
        print(f"Exists during block: {os.path.exists(path)}")

        # write a file inside it to prove cleanup works
        with open(os.path.join(path, "hello.txt"), "w") as f:
            f.write("test")

        print(f"File created inside: {os.listdir(path)}")

    print(f"Exists after block: {os.path.exists(path)}")
    print("done")

    try:
        with TempDir(prefix="crash_") as path:
            print(f"Created: {path}")
            raise ValueError("something broke")
    except ValueError as e:
        print(f"Caught: {e}")

    print(f"Exists after exception: {os.path.exists(path)}")
    
# Exercise on 
# JSON - javascript Object Notation

import json 
import numpy as np
from week_01_python_oop import DatasetProfile
from week_01_python_oop import ColumnProfile, CategoricalColumn, NumericColumnProfile

class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)

def save_profile(profile: DatasetProfile, path: str) -> None:
    columns = []
    for col in profile:
        columns.append({
            "name" : col.name,
            "dtype" : col.dtype,
            "null_rate" : col.null_rate,
            "is_clean" : col.is_clean
        })
        
    with open(path, 'w') as f:
        json.dump(columns, f, indent = 2, cls=AgentEncoder)
            
def load_profile(path: str) -> list[dict]:
    with open(path, 'r') as f:
        return json.load(f)
        
if __name__ == "__main__":
    #from data_agent.profiler import DatasetProfile, ColumnProfile

    profile = DatasetProfile()
    profile.add_column(ColumnProfile("id", "int64", 0, 5000))
    profile.add_column(ColumnProfile("revenue", "float64", 3, 5000))

    save_profile(profile, "profile.json")

    loaded = load_profile("profile.json")
    for col in loaded:
        print(col)
        

# Exercise 1 — Save and Load a Single Column
# Goal: Practice the bare minimum. One column → one dict → JSON file → back.
# Task
# Write a file called column_io.py with two functions:

class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)
    
def save_column(col: ColumnProfile, path: str) -> None:
    with open(path, 'w') as f:
        json.dump({
            "name" : col.name,
            "dtype" : col.dtype,
            "null_rate" : float(col.null_rate),
            "is_clean" : bool(col.is_clean)
        }, f, indent = 2, cls=AgentEncoder)
    
def load_column(path: str) -> ColumnProfile:
    with open(path, 'r') as f:
        data = json.load(f)
    return ColumnProfile(
        name=data["name"],
        dtype=data["dtype"],
        null_rate=data["null_rate"],
        is_clean=data["is_clean"] 
    )

if __name__ == "__main__":
    #from data_agent.profiler import ColumnProfile

    col = ColumnProfile("revenue", "float64", 3, 5000)
    save_column(col, "column.json")

    loaded = load_column("column.json")
    print(loaded)
    print(type(loaded))
