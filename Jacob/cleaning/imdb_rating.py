import imdb
import numpy as np 
import pandas as pd

df = pd.read_csv (r'netflix_titles.csv')

print(df)
ia = imdb.IMDb()
# name of the movie

# searching the name of the movie

titles = df["title"], df["release_year"]

print(titles[1][1])
print(len(titles[1]))

for i in range(len(df)-1):
    try:
        search = ia.search_movie(titles[0][i])
        for movie in search:
            try:
                if ((titles[0][i] == movie['title']) and (titles[1][i] == movie['year'])):
                    ID = movie.movieID
                    series = ia.get_movie(ID)
                    df.at[i,'IMDB_Rating'] = series['rating']
                    break 
            except:
                continue
    except:
        continue
    print("done " + str(i))
        
        
print(df["IMDB_Rating"])
