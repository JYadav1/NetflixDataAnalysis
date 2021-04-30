import pandas as pd 
import numpy as np

df = pd.read_csv (r'netflix_titles.csv')


film_types = df["listed_in"]

genres = {}
 
for i in range(len(df) - 1):
    try: 
        types = film_types[i]
        types = types.split(',')
        for t in types:
            if t[0] == " ":
                t = t.replace(' ', '', 1)

            if t in genres:
                count = genres[t]
                count += 1
                genres[t] = count
            else:
                genres[t] = 1
    except:
        continue

genres = pd.DataFrame(genres.items(), columns=['Genre', 'Occurance'])
genres = genres.sort_values(by=['Occurance'], ascending=False)
print(genres)

genres.to_csv('genres.csv', index=False)

