import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data


@st.cache
def load_data():
    #Loading pre-processed data
    df_countries_count = pd.read_csv('AmountOfNetflixContentProducedPerCountry.csv')
    df_netflix_titles = pd.read_csv('netflix_titles.csv')
    new_df = pd.read_csv('jacob/new_netflix.csv')
    actors = pd.read_csv('jacob/actors.csv')
    directors = pd.read_csv('jacob/directors.csv')
    genres = pd.read_csv('jacob/Genres.csv')
    avg_sent = pd.read_csv('jacob/avg_sentiment.csv')
    imdb_average = pd.read_csv('jacob/imdb_average.csv')

    return df_countries_count, df_netflix_titles, new_df, actors, directors, genres, avg_sent, imdb_average

df_countries_count, df_netflix_titles, new_df, actors, directors, genres, avg_sent, imdb_average = load_data()

# Create a Title for the App
st.markdown("<h1 style='text-align: center; color: red;'>Netflix Data Analysis</h1>", unsafe_allow_html=True)
st.write('  \n')




show = st.sidebar.radio("What Visualization do you want to show?", ['Amount of content produced per Country', 'Compare Netflix Content produced from years 1925 - 2021', 'Common Duration', 'cast', 'sentiment', 'genres', 'imdb_rating'])

if show == 'Amount of content produced per Country':
    # Get the json countries url in order to display the map.
    country_json = alt.topo_feature(data.world_110m.url, 'countries')

    countries_excluded = st.multiselect('What countries would you like to exclude?', df_countries_count['country'], key='choropleth')
    if len(countries_excluded) != 0:
        df_countries_count = df_countries_count[~df_countries_count['country'].isin(countries_excluded)]
    # Display a world map of the data for the first visualization.
    # Based on Amount of etflix content produced per country.

    netflix_map = alt.Chart(country_json).mark_geoshape().encode(
        color='count:Q',
        tooltip=['country:N', 'count:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_countries_count, 'id', ['count', 'country'])
    ).project(
        type='equirectangular'
    ).properties(
        width=600,
        height=800,
        title="Total Netflix Content Produced by each Country (1925-2021)"
    )
    netflix_map

if show == 'Compare Netflix Content produced from years 1925 - 2021':
    select_year = st.slider('Select a range of years', 1925, 2021, (1925, 2021))
    # Second visual
    df_type_year = df_netflix_titles.groupby(['type', 'release_year']).count().reset_index()
    df_movies = df_type_year[df_type_year['type'] == 'Movie']
    df_shows = df_type_year[df_type_year['type'] == 'TV Show']
    df_movies.set_index('release_year', inplace=True)
    df_shows.set_index('release_year', inplace=True)
    df_movies = df_movies.loc[select_year[0]:select_year[1], :].reset_index()
    df_shows = df_shows.loc[select_year[0]:select_year[1], :].reset_index()
    join = pd.concat([df_shows, df_movies],axis=0)
    # Create a Grouped Bar Chat
    chart = alt.Chart(join).mark_bar().encode(
        x=alt.X('type:O'),
        y='sum(show_id):Q',
        color='type:N',
        column='release_year:N'
    )

    st.write(chart)

if show == 'Common Duration':

    # Create a series that has the counts of movies(min) in duration
    df_movies_duration = df_netflix_titles[df_netflix_titles["type"] == "Movie"]["duration"].value_counts()
    # Create a series that has the counts of tvShows(Seasons) in duration
    df_shows_duration = df_netflix_titles[df_netflix_titles['type'] == 'TV Show']['duration'].value_counts()
    # Change the series into a dataframe
    df_movies_duration1 = pd.DataFrame({'duration':df_movies_duration.index, 'count':df_movies_duration.values})
    # Change the series into a dataframe
    df_shows_duration1 = pd.DataFrame({'duration':df_shows_duration.index, 'count':df_shows_duration.values})

    button = st.radio('Tv Shows or Movie? ',['Tv Shows', 'Movies'])
    if button == 'Tv Shows':
        # Creata a bar chart using altair
        chart_shows = alt.Chart(df_shows_duration1).mark_bar().encode(
            x=alt.X('duration', sort= '-y'),
            y='count'
        ).properties(
            title="The most common number of TV Show (Seasons) on Netflix"
        ).interactive()
        st.write(chart_shows)

    if button == 'Movies':

        # Creata a bar chart using altair
        chart_movies = alt.Chart(df_movies_duration1).mark_bar().encode(
            x=alt.X('duration', sort= '-y'),
            y='count'
        ).properties(
            title="The most common number of Movie (mins) on Netflix"
        ).interactive()

        st.write(chart_movies)
if show == 'cast':
    button1 = st.radio('Directors or Actors? ',['directors', 'actors'])

    if button1 == 'actors':
        top10_actors = actors.head(10)
        actors = alt.Chart(top10_actors).mark_bar().encode(x='Actor',y='Occurance')
        st.write(actors)

    if button1 == 'directors':
        top10_directors = directors.head(10)
        directors = alt.Chart(top10_directors).mark_bar().encode(
        x='Director',
        y='Occurance'
    )   
        st.write(directors)

if show == 'genres':
    genres = alt.Chart(genres).mark_bar().encode(x='Genre',y='Occurance')
    st.write(genres)

if show == 'sentiment':
    
    cols = ['Fear', 'Happy', 'Sad', 'Surprise', 'Angry']
    option = st.multiselect('What emotions do you want to display?', cols)

    avg_sent = avg_sent[avg_sent['Year'] >= 1980]
    chart_options = []

    if 'Fear' in option:
        fear = alt.Chart(avg_sent).mark_line().encode(x='Year',y='Fear', color=alt.value("orange"))
        chart_options.append(fear)
    if 'Happy' in option:
        happy = alt.Chart(avg_sent).mark_line().encode(x='Year',y='Happy',color=alt.value("yellow"))
        chart_options.append(happy)
    if 'Sad' in option:
        sad = alt.Chart(avg_sent).mark_line().encode(x='Year',y='Sad',color=alt.value("blue"))
        chart_options.append(sad)
    if 'Surprise' in option:
        surprise = alt.Chart(avg_sent).mark_line().encode(x='Year',y='Surprise',color=alt.value("green"))
        chart_options.append(surprise)
    if 'Angry' in option:
        angry = alt.Chart(avg_sent).mark_line().encode(x='Year',y='Angry',color=alt.value("red"))
        chart_options.append(angry)

    sentiment = alt.layer(*chart_options)

    st.write(sentiment)

if show == 'imdb_rating':
    imdb_average = imdb_average[imdb_average['Year'] >= 1980]
    imdb = alt.Chart(imdb_average).mark_line().encode(x='Year',y='IMDB_Rating',)
    st.write(imdb)
    
    
