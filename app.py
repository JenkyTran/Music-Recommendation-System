import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "fedf211aa18c4fc797b96f3cb5b82c06"
CLIENT_SECRET = "b149d46087364904a1f746b170b9b9ca"

# Khởi tạo Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set the background image and styles
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://e0.pxfuel.com/wallpapers/1016/985/desktop-wallpaper-snow-mountain-night-landscape-minimalist-minimalism.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.5);
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae;
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background-color: rgba(0, 0, 0, 0.7) !important;
    color: white;
}
</style>
"""
st.markdown(input_style, unsafe_allow_html=True)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = spotify.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def get_song_url(song_name):
    results = spotify.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track['external_urls']['spotify']
    else:
        return "#"


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_url = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_url.append(get_song_url(music.iloc[i[0]].song))

    return recommended_music_names, recommended_music_posters, recommended_music_url


st.title('🎵 Music Recommender System 2024 🎶')
st.write("Find your next favorite song based on the music you love!")

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox("Type or select a song from the dropdown", music_list)

if selected_music:
    # Tìm kiếm bài hát
    result = spotify.search(q=selected_music, type="track", limit=1)
    track = result["tracks"]["items"][0]

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(track['album']['images'][0]['url'], use_column_width=True)
    with col2:
        st.subheader(track['name'])
        st.write(f"**Artist:** {track['artists'][0]['name']}")
        st.write(f"**Album:** {track['album']['name']}")
        st.write(f"**Release Date:** {track['album']['release_date']}")
        st.write(f"[Listen on Spotify]({track['external_urls']['spotify']})")

if st.button('Show Recommendations'):
    recommended_music_names, recommended_music_posters, recommended_music_url = recommend(selected_music)
    for name, poster, url in zip(recommended_music_names, recommended_music_posters, recommended_music_url):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(poster, use_column_width=True)
        with col2:
            st.subheader(name)
            st.write(f"[Play on Spotify]({url})")
