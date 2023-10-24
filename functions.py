import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import requests

# Load the dataset
df = pd.read_csv('clean_spoti_data.csv')

def artist_pop():
    artist_popularity = df.groupby('Artist_Name')['Followers'].max().sort_values(ascending=False)
    artist_popularity=artist_popularity[:5]
    df2=pd.DataFrame(artist_popularity)
    df2=df2.reset_index()
    ImageUrl=['https://media.brstatic.com/2017/04/06171330/ed-sheeran-networth-mst.jpg','https://static.cinemagia.ro/img/db/actor/56/48/69/ariana-grande-826821l.jpg',
          'https://3.bp.blogspot.com/-qDfAM31MRnM/V_iBA1VZJlI/AAAAAAAAEhA/GKloBO7Bkx47O7c-vY3cD09E1-7iA2aHwCLcB/s1600/arijit-singh.jpg','https://specials-images.forbesimg.com/imageserve/1164343505/960x0.jpg?fit=scale',
          'https://th.bing.com/th/id/OIP.g3UUJOoDAKEpbv2pFqvEqwHaEK?pid=ImgDet&rs=1']
    df2['Image_Url']=ImageUrl
    return df2
def genre():
    genre_count_dict = {}

    # Create a DataFrame
    l = list(df['Genre'].unique())
    print(l)

    c=pd.DataFrame(l)
    c.columns=['Genre']
    # Iterate through each row in the DataFrame and count genres
    for row in c['Genre']:
        genres = eval(row)
        for genre in genres:
            if genre in genre_count_dict:
                genre_count_dict[genre] += 1
            else:
                genre_count_dict[genre] = 1

    # Display the genre counts in the dictionary
    for genre, count in genre_count_dict.items():
        print(f'{genre}: {count}')
    # Sort the genre counts to find the top 10 genres
    # Sort the genre counts to find the top 10 genres
    sorted_genres = sorted(genre_count_dict.items(), key=lambda item: item[1], reverse=True)

    # Create a DataFrame from the top 10 genres
    top_10_df = pd.DataFrame(sorted_genres[:10], columns=['Genre', 'Count'])

    # Create a horizontal bar chart using Altair
    chart = alt.Chart(top_10_df).mark_bar().encode(
        x='Count',
        y=alt.Y('Genre', sort='-x'),
        color=alt.value('#7FFFD4')
    ).properties(
        title='Top 10 Genres'
    )
    chart = chart.configure_legend(title=None)
    return chart

def album_release():
    df['Release date'] = pd.to_datetime(df['Release date'])

    # Extract the release year from the date
    df['Release Year'] = df['Release date'].dt.year

    # Group by release year and count the number of albums
    album_counts = df.groupby('Release Year').size().reset_index(name='Count')

    # Create an interactive line chart using Plotly
    fig = px.line(album_counts, x='Release Year', y='Count', title='Total Number of Albums Released Each Year')

    # Add interactivity for selecting data points
    fig.update_traces(mode='markers+lines', marker=dict(size=10), selector=dict(mode='event'))
    
    fig.update_traces(line_color='#00FF00')
    # Display the Plotly chart with select marking using st.plotly_chart
    return fig

def info():
    client_id = '8922e302101c4f2b9b73385efafb26d5'
    client_secret = 'f97e5f3575df49ceabf7804ce35c1d47'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    artist_name = st.text_input("Enter the artist name:")

    if artist_name:
        result = sp.search(artist_name, type='artist')
        if result['artists']['items']:
            artist = result['artists']['items'][0]
            st.sidebar.header(f'{artist["name"]}')
            st.sidebar.image(artist['images'][0]['url'], caption='', use_column_width=True)
            st.sidebar.subheader(f'Popularity: {artist["popularity"]}')
            st.subheader('Top Tracks')
            top_tracks = sp.artist_top_tracks(artist['id'])
            track_names = [track['name'] for track in top_tracks['tracks']]
            selected_track = st.selectbox('Select a track to play:', track_names)
            if selected_track:
                track_uri = top_tracks['tracks'][track_names.index(selected_track)]['uri']
                spotify_player_html = f'<iframe src="https://open.spotify.com/embed/track/{track_uri.split(":")[2]}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
                st.sidebar.markdown(spotify_player_html, unsafe_allow_html=True)

            st.subheader('Albums Published Every Year')
            albums = sp.artist_albums(artist['id'], album_type='album')
            years = [int(album['release_date'].split('-')[0]) for album in albums['items']]
            year_counts = {}
            for year in years:
                if year in year_counts:
                    year_counts[year] += 1
                else:
                    year_counts[year] = 1
            st.bar_chart(year_counts)
            st.subheader('Recommended Artists')
            
            related_artists = sp.artist_related_artists(artist['id'])

            # Extract recommended artist names and images
            recommended_artist_data = related_artists['artists']

            # Display recommended artists with small images
            st.subheader("Recommended Artists:")
            for i, artist_data in enumerate(recommended_artist_data):
                artist_name = artist_data['name']
                artist_uri = artist_data['external_urls']['spotify']
                artist_image = artist_data['images'][0]['url'] if artist_data['images'] else None

                # Create the URI hyperlink using Markdown
                artist_uri_markdown = f"[{artist_uri}]({artist_uri})"
                st.markdown(f"{i + 1}. {artist_name} - {artist_uri_markdown}")

                if artist_image:
                    # Fetch the image and resize it to 100x100 pixels
                    artist_image = Image.open(requests.get(artist_image, stream=True).raw)
                    artist_image = artist_image.resize((100, 100))
                    st.image(artist_image, caption=artist_name, use_column_width=False)
                else:
                    st.write("No image available for this artist.")
        