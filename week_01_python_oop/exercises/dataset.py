import pandas as pd
import numpy as np
from pathlib import Path
try:
    from .column import ColumnProfile, NumericColumn, CategoricalColumn
except ImportError:  # pragma: no cover - allows direct script execution.
    from column import ColumnProfile, NumericColumn, CategoricalColumn

class AgentEncoder:
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
        
        entry = {
            'name': path.name,
            'dtype': path.dtype,
            'null_rate': path.null_rate,
            'is_clean': path.is_clean
        }
        if isinstance(path, CategoricalColumn):
            entry['cardinality'] = int(path.cardinality)
        if isinstance(path, NumericColumn):
            entry['mean'] = float(path.mean)
            entry['std'] = float(path.std)
        
        with open(path, 'w') as f:                
            json.dump(entry, f, indent=2, cls=AgentEncoder)
            
    def from_json(cls, path: Path) -> DatasetProfile:
        with open(path, 'r') as f:
            return json.load(f)
        
    def to_csv(self, path: Path) -> None:
        with open(path, 'w', newline="") as f:
            writer = csv.DictWriter(f)
            
            
if __name__ == "__main__":
    
    def run_demo():
        #import pandas as pd
        df = pd.DataFrame({'revenue': [100, 200, None], 'country': ['ET', 'US', 'ET']})
        profile = DatasetProfile.from_dataframe(df)
        profile.quality_report() 
        profile.to_csv()
        
    run_demo()
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
