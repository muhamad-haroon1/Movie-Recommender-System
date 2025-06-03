import os
import pickle
import streamlit as st
import pandas as pd

# Get the folder path where this script is located
BASE_DIR = os.path.dirname(__file__)

# Load movie data
movies_dict_path = os.path.join(BASE_DIR, 'movies_dict.pkl')
movies_dict = pickle.load(open(movies_dict_path, 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')
similarity = pickle.load(open(similarity_path, 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    # Sorting movies based on similarity scores (excluding the selected movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Fetching movie titles
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    
    return recommended_movies

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Gradient background */
    .stApp {
        background: linear-gradient(135deg, #1f4037, #99f2c8);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
    }
    
    /* Title styling */
    .title {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        color: #ffffff;
        text-shadow: 3px 3px 7px rgba(0,0,0,0.7);
        margin-bottom: 5px;
    }

    /* Subtitle styling */
    .subtitle {
        font-size: 22px;
        text-align: center;
        color: #e0e0e0;
        margin-bottom: 30px;
        font-style: italic;
    }

    /* Button styling */
    div.stButton > button:first-child {
        background: #2ecc71;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 25px;
        font-size: 18px;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.3);
        transition: background-color 0.3s ease;
        margin: 0 auto;
        display: block;
    }

    div.stButton > button:first-child:hover {
        background: #27ae60;
        cursor: pointer;
    }

    /* Recommendation cards */
    .recommendation {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px auto;
        width: 60%;
        text-align: center;
        font-size: 20px;
        color: #f0f0f0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        font-weight: 600;
    }

    /* Center the selectbox */
    .stSelectbox > div {
        justify-content: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Display Title
st.markdown('<p class="title">🎬 Movie Recommender System</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover movies tailored just for you! 🍿</p>', unsafe_allow_html=True)

# Movie Selection - centered
Selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values,
    index=0,
    key='movie_select'
)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(Selected_movie_name)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>Top recommendations based on <em>{Selected_movie_name}</em>:</h3>", unsafe_allow_html=True)
    for movie in recommendations:
        st.markdown(f'<div class="recommendation">{movie}</div>', unsafe_allow_html=True)
