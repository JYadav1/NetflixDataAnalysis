import pandas as pd 
import numpy as np
from pytrends.request import TrendReq


df = pd.read_csv (r'netflix_titles.csv')

df["month_trend"] = np.nan
df["year_trend"] = np.nan

pytrends = TrendReq(hl="en-US", tz=360, retries=10, backoff_factor=0.5)
time = "today 1-m"
cat = "0"
geo = "US"
gprop = ""
keywords = []






def get_trends(title,category):
    pytrends.build_payload(title, cat=category, timeframe=time, geo="US", gprop="")
    data = pytrends.interest_over_time()
    mean = data[keyword[0]].mean()
    mean = round(mean, 3)
    return (mean)
    


#ticker=df.iat[i, 0]
print(df)
for index, film in df.iterrows():
    keyword = [film["title"],]
    try:
        if (film["type"] == "TV Show"):
            category = 36
            trend = get_trends(keyword, category)
            
        if (film["type"] == "Movie"):
            category = 34
            trend = get_trends(film["title"], category)
        
        film["month_trend"] = trend
        
    except:
        film["month_trend"] = 0
    print(film["month_trend"])

print("done")
df.to_csv('netflix_with_trends.csv', index=False)

 
        
        
    


