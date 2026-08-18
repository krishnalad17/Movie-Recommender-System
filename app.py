import streamlit as st
import joblib
import requests

movies = joblib.load('movies.pkl')
similarity = joblib.load('similarity.pkl')


def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMTJlZmE1MTZlZmRjM2M0M2E1MzAzNzdiZjY2YzlkNiIsIm5iZiI6MTc4Njk1NjU4OS4zMTksInN1YiI6IjZhODJjYjJkYTRmNTkwMGE4MTAyMjMyYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4w0713ysDMIQn-1v6jTIKqYszCERVPPLDKyYgPq5DHM"
    }

    params = {
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=(5, 20)
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except requests.exceptions.RequestException as e:
        print(f"TMDB error for {movie_id}: {e}")

    return None

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_movies_poster = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].id

        recommend_movies.append(
            movies.iloc[i[0]].title
        )

        recommend_movies_poster.append(
            fetch_poster(movie_id)
        )

    return recommend_movies, recommend_movies_poster


movies_list = movies['title'].values

st.title('Movie Recommender System')

option = st.selectbox(
    'Select a movie',
    movies_list
)

if st.button('Recommend'):

    recommended_movie_names, recommended_movie_posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        if recommended_movie_posters[0]:
            st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        if recommended_movie_posters[1]:
            st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        if recommended_movie_posters[2]:
            st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        if recommended_movie_posters[3]:
            st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        if recommended_movie_posters[4]:
            st.image(recommended_movie_posters[4])