import pandas as pd
import json
import dataset
import column
from column import ColumnProfile, NumericColumn, CategoricalColumn
from dataset import DatasetProfile

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


# Serializing the profile to JSON
class AgentEncoder(json.JSONEncoder):
    columns = [{}]
    def save_profile(profile: DatasetProfile, path: str) -> None:
        if isinstance (profile, Datasetprofile):
            data = {
                "columns": [
                    {
                    "name": col.name,
                    "dtype": col.dtype,
                    "null_count": col.null_count,
                    "total_count": col.total_count
                }
                    for col in profile.columns]
            }
            with open(path, 'w') as f:
                json.dump(data, f, indent = 2, cls=AgentEncoder)
                
    def load_profile(path: str) -> list[dict]:
        with open(path, 'r') as f:
            data = json.load(f)    
        return data

if __name__ == "__main__":
    #from data_agent.profiler import DatasetProfile, ColumnProfile

    profile = DatasetProfile()
    profile.add_column(ColumnProfile("id", "int64", 0, 5000))
    profile.add_column(ColumnProfile("revenue", "float64", 3, 5000))

    save_profile(profile, "profile.json")

    loaded = load_profile("profile.json")
    for col in loaded:
        print(col)