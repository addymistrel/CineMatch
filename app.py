import os
import pickle
import streamlit as st
import pandas as pd
import requests
import gdown

def fetch_poster(title):
    url = "http://www.omdbapi.com/?apikey=c9eb1bb2&t={}".format(title)
    data = requests.get(url)
    data = data.json()
    poster_path = data['Poster']
    full_path = poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

def display(names, posters):
    for i in range(0, len(names), 2):
        col1, col2 = st.columns(2)
        with col1:
            st.text(names[i])
            st.image(posters[i])
        with col2:
            if i + 1 < len(names): 
                st.text(names[i + 1])
                st.image(posters[i + 1])

# Check if files exist, if not download from Google Drive
movies_dict_path = 'movies_dict.pkl'
similarity_path = 'similarity.pkl'

if not os.path.exists(movies_dict_path):
    gdown.download('https://drive.google.com/uc?id=1NSO2tEC4Zsz0VXf5g8PbtD_8kP7esskc', movies_dict_path, quiet=False)

if not os.path.exists(similarity_path):
    gdown.download('https://drive.google.com/uc?id=1SvntVZCEUEVY87XP6-3_SwEhoO7TCn2s', similarity_path, quiet=False)

# Load the data
movies_dict = pickle.load(open(movies_dict_path, 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(similarity_path, 'rb'))

st.set_page_config(page_title="CineMatch", page_icon=":rocket:")
st.header('CineMatch - A Movie Recommender System', divider="rainbow")

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    display(recommended_movie_names, recommended_movie_posters)
