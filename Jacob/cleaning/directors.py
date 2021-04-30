import pandas as pd 
import numpy as np

df = pd.read_csv (r'netflix_titles.csv')


filmers = df["director"]

directors = {}
 
for i in range(len(df) - 1):
    try: 
        some_dudes = filmers[i]
        some_dudes = some_dudes.split(',')
        for name in some_dudes:
            if name in directors:
                count = directors[name]
                count += 1
                directors[name] = count
            else:
                directors[name] = 1
    except:
        continue

directors = pd.DataFrame(directors.items(), columns=['Director', 'Occurance'])
directors = directors.sort_values(by=['Occurance'], ascending=False)
print(directors)
directors.to_csv('directors.csv', index=False)