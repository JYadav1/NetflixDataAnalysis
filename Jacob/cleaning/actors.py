import pandas as pd 
import numpy as np

df = pd.read_csv (r'netflix_titles.csv')


cast = df["cast"]

actors = {}

for i in range(len(df) - 1):
    try: 
        names = cast[i]
        names = names.split(',')
        for name in names:
            if name in actors:
                count = actors[name]
                count += 1
                actors[name] = count
            else:
                actors[name] = 1
    except:
        continue

actors = pd.DataFrame(actors.items(), columns=['Actor', 'Occurance'])
actors = actors.sort_values(by=['Occurance'], ascending=False)
print(actors)
actors.to_csv('actors.csv', index=False)