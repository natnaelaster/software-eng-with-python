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