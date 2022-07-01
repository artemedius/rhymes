import pronouncing

with open('if.txt') as f:
    while True:
        line = f.readline()
        if not line: 
            break
        print(line) 