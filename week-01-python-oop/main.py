import dataset
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