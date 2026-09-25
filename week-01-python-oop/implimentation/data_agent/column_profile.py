import pandas as pd

class ColumnProfile:

    def __init__(self, name: str, dtype: str, null_count: int, total_count:int):
        
        if null_count < 0:
            raise ValueError(f"null_count must be >= 0, got {null_count}")
        if null_count > total_count:
            raise ValueError(f"null_count ({null_count}) cannot exceed total_count ({total_count})")

        self.name = name
        self.dtype = dtype
        self.null_count = null_count
        self.total_count = total_count

    def __repr__(self) -> str:
        return (f"ColumnProfile(name={self.name!r}, dtype={self.dtype!r}, "
                f"null_count={self.null_count}, total_count={self.total_count})")

    def __str__(self) -> str:
        return f"Column '{self.name}' [{self.dtype}] — {self.null_rate:.1%} null"    


    def summary(self) -> str:
        return f"{self.name} [{self.dtype}] — {self.null_rate:.1%} null"

    @property
    def null_rate(self) -> float:
        if self.total_count == 0:
            return 0
        return self.null_count / self.total_count  

    @property
    def is_clean(self) -> bool:
        return self.null_rate < 0.05

    @classmethod
    def from_series(cls, series: pd.Series, name: str) -> 'ColumnProfile':
        if name is None: 
            name = series.name if series.name is not None else 'unnamed'
        return cls(
            name = name,
            dtype = str(series.dtype),
            null_count = int(series.isna().sum()),
            total_count = len(series)
        )
    # Add __lt__ to ColumnProfile so a list of columns can be sorted by null rate
    def __lt__(self, other: 'ColumnProfile') -> bool:
        if not isinstance(other, ColumnProfile):
            return NotImplemented
        return self.null_rate < other.null_rate
        

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
            
            if pd.api.types.is_numeric_dtype(series):
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
        for col in self._columns:
            if col.name == name:
                return col
        raise KeyError(f"Column '{name}' not found")        

class NumericColumn(ColumnProfile):
    def __init__(self, name, dtype, null_count, total_count, mean: float, std: float):
        super().__init__(name, dtype, null_count, total_count)
        self.mean = mean
        self.std = std

    def summary(self) -> str:
        return f"{self.name} [{self.dtype}] — {self.null_rate:.1%} null | mean={self.mean:.2f}, std={self.std:.2f}"

class CategoricalColumn(ColumnProfile):
    def __init__(self, name, dtype, null_count, total_count, cardinality: int):
        super().__init__(name, dtype, null_count, total_count)
        self.cardinality = cardinality

    def summary(self) -> str:
        return f"{self.name} [{self.dtype}] — {self.null_rate:.1%} null | cardinality = {self.cardinality}"
    
    
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