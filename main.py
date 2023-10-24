import streamlit as st
from functions import *
# Load the dataset

st.set_page_config(
    page_title='Spotisimplify',
    page_icon='spotify-logo-streaming-media-apple-music-others.jpg'
)
st.markdown(
    """
    <style>
    body {
        background-color: lightgray;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    page = st.selectbox("", ["Home","Artist Popularity", "Genre Distribution","Album Release Analysis","Individual Artist info"])

# 1. Artist Popularity
if page=="Home":
    st.markdown(
    """
    <style>
    body {
        background-color: lightgray;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Display the Spotify logo as an image in the first column
    st.image('https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png', width=270)

    # Write some information about Spotify
    st.markdown("### Spotify is a popular music streaming platform that offers a vast library of songs, playlists, and podcasts. "
            "It allows users to discover and enjoy music from various genres and artists. Spotify provides both free and premium subscription options, "
            "with features like offline listening, ad-free music, and more. It's available on various devices and platforms, "
            "making it a versatile choice for music lovers worldwide.")
if page=="Artist Popularity":
    st.header('Top 5 Artists')
    artist_popularity = artist_pop()
    for i, row in artist_popularity.iterrows():
        st.markdown(f"### {row['Artist_Name']}")
        st.image(row['Image_Url'], caption='',width=300)

# 2. Genre Distribution
if page=="Genre Distribution":
    st.header('Top Genres on Spotify')
    img=genre()
    # Display the Altair chart using st.altair_chart
    st.altair_chart(img, use_container_width=True)

if page=='Album Release Analysis':
# 3. Album Release Analysis
    st.header('Album Release Timeline')
    fig=album_release()
    st.plotly_chart(fig, use_container_width=True)

if page=='Individual Artist info':
    st.title("Spotify Artist Information")
    info()

       
        




