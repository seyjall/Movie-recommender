import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')
similarity = pickle.load(open('similarity.pkl' ,'rb' ))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key=fc1bb5b46712b8f459d907ab2083d2be"
    try:
        res = requests.get(url)
        data = res.json()
        poster_path = data['posters'][0]['file_path']
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        if poster_path:
            return image_url
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True , key = lambda x:x[1])[1:6]

    recommended_movies =[]
    recommended_movies_posters = []
    for i in movies_list :
       recommended_movies.append(movies.iloc[i[0]].title)
       recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies , recommended_movies_posters




movies_dict = pickle.load(open('movie_dict.pkl' ,'rb' ))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie = st.selectbox('Search Your Favourite Movie' ,
movies['title'].values)

if st.button('Recommend'):
    names , posters =  recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        if names[i] and posters[i]:
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
        elif names[i]:
            with cols[i]:
                st.text(names[i])
                st.write("No image available")
        else :
            with cols[i]:
                st.write("No data available")

