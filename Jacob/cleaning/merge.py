import pandas as pd

df1 = pd.read_csv (r'netflix_titles.csv')
df2 = pd.read_csv (r'netflix_IMDB_scores.csv')
df3 = pd.read_csv (r'netflix_sentiment_scores.csv')

df4 = df1.combine_first(df2)
df5 = df4.combine_first(df3)

df5.to_csv('new_netflix.csv', index=False)

print(df5)