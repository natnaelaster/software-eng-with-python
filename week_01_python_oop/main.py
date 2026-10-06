import pandas as pd
import json
import dataset
import column
from column import ColumnProfile, NumericColumn, CategoricalColumn
from dataset import DatasetProfile

'''
# Create sample data
df = pd.DataFrame({
    'name': ['Alice', 'Bob', None, 'David'],
    'age': [25, 30, 22, None],
    'score': [85.5, 92.3, 78.1, 89.7]
})

# Build profile
profile = DatasetProfile.from_dataframe(df)

# Print quality report
profile.quality_report()

# Access clean columns
print("Clean columns:", [col.name for col in profile.clean_columns])

# Create single column profile manually
col = ColumnProfile('age', 'int64', 1, 4)
print(col)
print(repr(col))
print(len(profile))
print('Alice' in profile) '''


# Serializing the profile to JSON
class AgentEncoder(json.JSONEncoder):
    """Extends the default JSON encoder to handle NumPy types."""
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)
    
def save_profile(profile: DatasetProfile, path: str) -> None:
    """Save the columns of a DatasetProfile to a JSON file."""
    columns = []
    for col in profile:
        columns.append({
            "name": col.name,
            "dtype": col.dtype,
            "null_rate": float(col.null_rate),
            "is_clean": bool(col.is_clean)
        })
    
    with open(path, 'w') as f:
        json.dump(columns, f, indent=2, cls=AgentEncoder)
            
def load_profile(path: str) -> list[dict]:
    """Load the list of column dicts from a JSON file."""
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
    #Takes a single column object (a ColumnProfile) and a path.
    #Serializes just that one column into a dict with:
    entry = {
            "name" : col.name,
            "dtype" : col.dtype,
            "null_rate" : float(col.null_rate),
            "is_clean" : bool(col.is_clean)
            }
    
    with open(path, 'w') as f:
        json.dump(entry, f, indent = 2, cls=AgentEncoder)
    
def load_column(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    

    #from data_agent.profiler import ColumnProfile

    col = ColumnProfile("revenue", "float64", 3, 5000)
    save_column(col, "column.json")

    loaded = load_column("column.json")
    print(loaded)
    print(type(loaded)) 

# Exercise 2 — Multiple Columns From Different Types
# Goal: Reinforce polymorphism in JSON. Save a mixed list of columns (base and subclasses) and load it back.
# Task
# Write a file called multi_column_io.py with two functions:    

'''
class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)
    
# Function 1: save_columns(columns, path)
def save_columns(columns: list[ColumnProfile, CategoricalColumn, NumericColumn], path: str) -> None:
    cols = []
    for col in columns:
        if isinstance(col, ColumnProfile): 
            cols.append({
                "name" : col.name,
                "dtype" : col.dtype,
                "null_rate" : float(col.null_rate),
                "is_clean" : bool(col.is_clean)
        })
        if isinstance(col,CategoricalColumn):
            cols.append({
                "name" : col.name,
                "dtype" : col.dtype,
                "null_rate" : float(col.null_rate),
                "is_clean" : bool(col.is_clean),
                "cardinality" : col.cardinality
            })
        if isinstance(col, NumericColumn):
            cols.append({
                "name" : col.name,
                "dtype" : col.dtype,
                "null_rate" : float(col.null_rate),
                "is_clean" : bool(col.is_clean),
                "mean" : float(col.mean),
                "std" : float(col.std)
            })
            
    with open(path, 'w') as f:
        json.dump(cols, f, indent=2, cls=AgentEncoder)

def load_columns(path: str) -> list[dict]:
    with open(path, 'r') as f:
        return json.load(f)
    
if __name__ == "__main__":
    column = [
        ColumnProfile("id", "int64", 0, 5000),
        CategoricalColumn("country", "object", 12, 5000, 87),
        NumericColumn("revenue", "float64", 3, 5000, 1420.5, 340.2)
    ]
    
    save_columns(column, "columnal.json")
    load = load_columns("columnal.json")
    for col in load:
        print (col) 

'''
class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)
    
# Function 1: save_columns(columns, path)
def save_columns(columns, path):
    result = []
    for col in columns:
        entry = {
            "name": col.name,
            "dtype": col.dtype,
            "null_rate": float(col.null_rate),
            "is_clean": bool(col.is_clean),
        }
        if isinstance(col, CategoricalColumn):
            entry["cardinality"] = int(col.cardinality)
        if isinstance(col, NumericColumn):
            entry["mean"] = float(col.mean)
            entry["std"] = float(col.std)
        result.append(entry)

    with open(path, "w") as f:
        json.dump(result, f, indent=2, cls=AgentEncoder)            

def load_columns(path: str) -> list[dict]:
    with open(path, 'r') as f:
        return json.load(f)
    
if __name__ == "__main__":
    column = [
        ColumnProfile("id", "int64", 0, 5000),
        CategoricalColumn("country", "object", 12, 5000, 87),
        NumericColumn("revenue", "float64", 3, 5000, 1420.5, 340.2)
    ]
    
    save_columns(column, "columnal.json")
    load = load_columns("columnal.json")
    for col in load:
        print (col)  
        

        
class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)  

def append_column(col: ColumnProfile, path: str) -> None:
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
    else:
        data = []
        
    entry = {
        "name": col.name,   
        "dtype": col.dtype,
        "null_rate": float(col.null_rate),
        "is_clean": bool(col.is_clean),
    }
    data.append(entry)
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, cls=AgentEncoder)

if __name__ == "__main__":
    import os

    path = "appended.json"
    if os.path.exists(path):
        os.remove(path)

    append_column(ColumnProfile("id", "int64", 0, 5000), path)
    append_column(ColumnProfile("revenue", "float64", 3, 5000), path)
    append_column(ColumnProfile("country", "object", 12, 5000), path)

    with open(path, "r") as f:
        print(f.read()) 
