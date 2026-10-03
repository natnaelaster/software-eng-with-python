# writing report text file
with open('report.txt', 'w') as f:
    f.write('dataset quality report\n')
    
with open('report.txt', 'a') as f:
    f.write('='*30 + '\n')
    f.write('null rate: 0.24%\n')
    f.write('clean column: 12 / 15\n')


# Read as one string    
with open('report.txt', 'r') as f:
    content = f.read()
print(content)

# read line by line
with open('report.txt', 'r') as f:
    for line in f:
        print(f'line: {line.strip()}')

# read in to a list
with open('report.txt', 'r') as f:
    content = f.readlines()
    
print (content)

if __name__ == '__main__':
    with open('score.txt', 'w') as f:
        f.write('Alice 95\n')
        f.write('Bob 87\n')
        f.write('Charlie 92\n')
        f.write('Diana 78\n')
        f.write('Eve 99\n')
        
    with open('score.txt', 'r') as f:
        av_score = 0
        count = 0
        for line in f:
            name, score = line.split()
            av_score += int(score)
            count += 1
            print(f'{name} scored {score}')
        print(f'Average score: {av_score / count:.2f}')
            

if __name__ == '__main__':
    import json
    
    profile_data = {
        "name": "sales_q4",
        "rows": 250000,
        "columns": 18,
        "clean": True,
        "null_rates": {"reavenue": 0.02, "country": 0.0}
    }
    
json_string = json.dumps(profile_data, indent=2)
print(json_string) 

loaded = json.loads(json_string)
print(loaded["name"])

with open('profile.json', 'w') as f:
    json.dump(profile_data, f, indent=2)
    
with open('profile.json', 'r') as f:
    loaded = json.load(f)
    
if __name__ == '__main__':
    import dataset
    from dataset import DatasetProfile
    import numpy
    
    df = pd.DataFrame({
    'name': ['Alice', 'Bob', None, 'David'],
    'age': [25, 30, 22, None],
    'score': [85.5, 92.3, 78.1, 89.7]
    })
    
    profile = DatasetProfile.from_dataframe(df)
    json.dump(profile)
    '''
    class AgentEncoder(json.JSONEncoder):
        def save_profile(self, profile: DatasetProfile, path: str) -> None:
            if isinstance(profile, np.floatiing):
                return float(profile)
            if isinstance(profile, np.integer):
                return int(profile)
            return super().save_profile(profile)

        def load_profile(path: str) -> list[dict]:
            pass'''


        