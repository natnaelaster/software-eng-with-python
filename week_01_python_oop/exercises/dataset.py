import pandas as pd
import numpy as np
import json
import csv
from pathlib import Path
from column import ColumnProfile, NumericColumn, CategoricalColumn

# New Class
class AgentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)

class DatasetProfile:

    def __init__(self):
        self._columns: list[ColumnProfile] = []

    def add_column(self, col_profile: ColumnProfile) -> None:
        self._columns.append(col_profile)

    @property
    def clean_columns(self) -> list[ColumnProfile]:
        return [col for col in self._columns if col.is_clean]

    def quality_report(self) -> None:
        print('\n' + '='*50)
        print('Data Set Quality')
        print('+'*50)

        for col in self._columns:
            grade = 'clean' if col.is_clean else 'needs attention'
            print(f'{col.name:20} {col.null_rate:10.2%} {grade}')

        print('-'* 50)
        total = len(self._columns)  
        clean = len(self.clean_columns)    
        if total > 0:
            print(f"Total columns : {total}")
            print(f"Clean columns : {clean} ({clean / total * 100:.1f}%)")
        else:
            print("No columns profiled.")
        print('=' * 50 + '\n')     

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> 'DatasetProfile':
        profile = cls()
        for col_name in df.columns:
            series = df[col_name]
            
            if pd.api.types.is_numeric_dtype(series):  # is the right tool — cleaner than checking dtype strings manually.
                col = NumericColumn(
                    name=col_name,
                    dtype=str(series.dtype),
                    null_count=int(series.isna().sum()),
                    total_count=len(series),
                    mean=round(float(series.mean()), 2),
                    std=round(float(series.std()), 2),
                )
            elif series.dtype in ('object', 'category'):
                col = CategoricalColumn(
                    name=col_name,
                    dtype=str(series.dtype),
                    null_count=int(series.isna().sum()),
                    total_count=len(series),
                    cardinality=int(series.nunique()),
                )
            else:
                col = ColumnProfile.from_series(series, col_name)
            
            profile.add_column(col)
        return profile


    def __add__(self, other: 'DatasetProfile') -> 'DatasetProfile':
        merged = DatasetProfile()
        for col in self:
            merged.add_column(col)
        for col in other:
            merged.add_column(col)
        return merged         

    def  __len__(self) -> int:
        return len(self._columns)

    def __contains__(self, name: str) -> bool:
        return any(col_profile.name == name for col_profile in self._columns)       

    def __iter__(self):
        return iter(self._columns)

    def __getitem__(self, name: str) -> ColumnProfile:
        for col in self._columns:          # _columns, not col_profiles
            if col.name == name:
                return col
        raise KeyError(f"Column {name!r} not found")
    
    def to_json(self, path: Path) -> None:
        """Write the profile as a JSON file."""
        entries = []
        for col in self:
            entry = {
                'name': col.name,
                'dtype': col.dtype,
                'null_count': col.null_count,
                'total_count': col.total_count,
                'null_rate': float(col.null_rate),
                'is_clean': bool(col.is_clean),
                'type': col.__class__.__name__,
            }        
            entries.append(entry)
            
        with open(path, 'w') as f:
            json.dump(entries, f, indent=2, cls=AgentEncoder)
    
    @classmethod      
    def from_json(cls, path: Path) -> "DatasetProfile":
        """Build a DatasetProfile from a JSON file."""
        with open(path, 'r') as f:
            entries = json.load(f)
        
        profile = cls() 
        for entry in entries:
            col = ColumnProfile(
                entry['name'],
                entry['dtype'],
                null_count=0,
                total_count=1,
            )
            profile.add_column(col)
        
        return profile
    
    def to_csv(self, path: Path) -> None:
        """Write the profile as a CSV quality report."""
        fieldnames = ["name", "dtype", "null_rate", "is_clean", "type"]
        
        with open(path, 'r') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for col in self:
                writer.writerow({
                    'name': col.name,
                    'dtype': col.dtype,
                    'null_rate': col.null_rate,
                    'is_clean': col.is_clean,
                    'type': col.__class__.__name__,
                })     
            
if __name__ == "__main__":
    '''
    run_demo()
    
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
    print('Alice' in profile) 
    print(to_json(col))
    
    #from data_agent.profiler import ColumnProfile
'''
    # testing to_json function  
    profile = DatasetProfile()
    profile.add_column(ColumnProfile("id", "int64", 0, 5000))
    profile.add_column(NumericColumn("revenue", "float64", 3, 5000, 1420.5, 340.2))

    profile.to_json(Path("test.json"))
        
    # testing from_json function
    loaded = DatasetProfile.from_json("test.json")
    print(len(loaded))
    for col in loaded:
        print(col.name, col.__class__.__name__) 
        
    # testing to_csv function
    loaded.to_csv(Path("test.csv"))