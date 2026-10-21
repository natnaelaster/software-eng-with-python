# Exercise on 
# Error Handling
# Costome exeptions
# Defensive programing

#exeptions
# 1
try:
    x = int("hello")
except ValueError as e:
    print(type(e).__name__)
    print(str(e)) 
    
# 2


