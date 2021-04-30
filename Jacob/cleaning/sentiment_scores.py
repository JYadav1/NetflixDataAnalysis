import pandas as pd
import text2emotion as te
import numpy as np
df = pd.read_csv (r'netflix_titles.csv')

df["Happy"] = np.nan
df["Angry"] = np.nan
df["Surprise"] = np.nan
df["Sad"] = np.nan
df["Fear"] = np.nan




def get_emotions(descriptions,df):
    index = 0
    for text in descriptions:
        words = text
        print(words)
        emotion = te.get_emotion(words)
        print(emotion)
        df.at[index,'Happy']= emotion['Happy']
        df.at[index,'Angry']= emotion['Angry']
        df.at[index,'Surprise']= emotion['Surprise']
        df.at[index,'Sad']= emotion['Sad']
        df.at[index,'Fear']= emotion['Fear']
        index += 1


descriptions = df["description"]
get_emotions(descriptions, df)
df.to_csv('netflix_sentiment_scores.csv', index=False)
print(df)


