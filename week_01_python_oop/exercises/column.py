import pandas as pd

#CLEAN_THERSHOLD = 0.05


# custome class for raising exceptions.
class DataAgentError(Exception):
    """Base for all errors in the data_agent package."""
    pass
class ProfilerError(DataAgentError):
    """Raised when profile-related failures occur."""
    pass
class InvalidColumnError(ProfilerError):
    """Raised when column validation fails."""
    pass
class ColumnProfile:
    def __init__(self, name: str, dtype: str, null_count: int, total_count:int):
        if not isinstance(name, str) or not name.strip():
            raise InvalidColumnError(f"name must be non-empty string, got {name!r}")
        if total_count <= 0:
            raise InvalidColumnError(f"total_count must be > 0, got {total_count}")
        if null_count < 0:
            raise InvalidColumnError(f"null_count must be >= 0, got {null_count}")
        if null_count > total_count:
            raise InvalidColumnError(f"null_count ({null_count}) cannot exceed total_count ({total_count})")
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
    
if __name__ == "__main__":
    # test code for custome exceptions. 
    try:
        profile = ColumnProfile('data', 'int64', -3, 40)
        print(profile.summary())
    except ProfilerError as e:
        print(f'caught through ProfilerError: {e}')
        