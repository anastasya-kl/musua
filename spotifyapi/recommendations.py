import warnings
warnings.filterwarnings("ignore")

""" --- IMPORTING --- """
OMP_NUM_THREADS=1
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

from sklearn.cluster import DBSCAN
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer

import numpy as np
import random
from collections import Counter

from sklearn.cluster import OPTICS
from sklearn.preprocessing import LabelEncoder

# --- IMPORT USER MODULES ---
from user         import *
from get_data     import *
from order_data   import *
from manage_data  import *
from convert_data import *
from content_data import *

def get_user_tastes_data(cursor, user_id):

    favourite_songs_ids     = get_songs_from_favourite(cursor, user_id)
    favourite_albums_ids    = get_albums_from_favourite(cursor, user_id)
    favourite_playlists_ids = get_playlists_from_favourite(cursor, user_id)
    
    songs_ids = set()
    
    #  ------------------------------------------------------------------
    if favourite_songs_ids:
        for album_id in favourite_albums_ids:
            songs_ids.update(get_songs_by_album(cursor, album_id))
    
    if favourite_playlists_ids:
        for playlist_id in favourite_playlists_ids:
            songs_ids.update(get_songs_by_playlist(cursor, playlist_id))
        
    if not songs_ids: return False
    
    songs_ids = list(songs_ids)

    full_artist_ids = []
    for song_id in songs_ids:
        full_artist_ids.append(get_artist_by_song(cursor, song_id))
        
    artist_ids = list(set(full_artist_ids))
     
    genres = []
    for artist_id in full_artist_ids:
        genres_by_artist = get_genres_by_artist(cursor, artist_id)
        if genres_by_artist is not None:
            genres += genres_by_artist

    Q1 = np.percentile(genres, 30)
    Q3 = np.percentile(genres, 70)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    genres_without_outliers = [x for x in genres if x >= lower_bound and x <= upper_bound]
    
    data = {
        'user_id'    : user_id,
        'genres_ids' : genres_without_outliers,
        'artist_ids' : artist_ids,
        'songs_ids'  : songs_ids,
        'full_artist_ids'         : full_artist_ids,
        'favourite_albums_ids'    : favourite_albums_ids,
        'favourite_playlists_ids' : favourite_playlists_ids
    }
    
    return data

def remove_outliers(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    cleaned_data = [x for x in data if lower_bound <= x <= upper_bound]
    return cleaned_data

def create_recommendations_OPTICS(cursor, main_user_data, min_samples=3):
    user_id = main_user_data['user_id']

    get_all_users_query = """SELECT id FROM users"""
    cursor.execute(get_all_users_query)
    rows = cursor.fetchall()
    user_ids = [row[0] for row in rows if row[0] != user_id]
    all_users_tastes = [main_user_data]
    user_ids_copy = user_ids
    
    for some_user_id in user_ids_copy:
        # print(f"{some_user_id}")
        user_tastes_data = get_user_tastes_data(cursor, some_user_id)
        if not user_tastes_data: 
            user_ids.remove(some_user_id)
            continue
        all_users_tastes.append(user_tastes_data)

    le = LabelEncoder()
    all_artists_with_outliers = [artist_id for user_data in all_users_tastes for artist_id in user_data['artist_ids']]
    le.fit(all_artists_with_outliers)

    cleaned_user_data = []
    for user_data in all_users_tastes:
        cleaned_artist_ids = remove_outliers([le.transform([artist_id])[0] for artist_id in user_data['artist_ids']])
        cleaned_user_data.append({'artist_ids': cleaned_artist_ids})

    artist_matrix = [user_data['artist_ids'] for user_data in cleaned_user_data]

    max_length = max(len(row) for row in artist_matrix)

    avg_values = np.mean([row + [0] * (max_length - len(row)) for row in artist_matrix], axis=0)
    artist_matrix_padded = [row + list(avg_values[len(row):]) for row in artist_matrix]

    optics = OPTICS(min_samples=min_samples)
    optics.fit(artist_matrix_padded)
    main_user_cluster = optics.labels_[0]

    similar_users = [i for i, cluster in enumerate(optics.labels_) if cluster == main_user_cluster]
    similar_users_data = [all_users_tastes[i] for i in similar_users]

    recommended_artists = set()
    for user_data in similar_users_data:
        for artist_id in user_data['artist_ids']:
            if artist_id not in main_user_data['artist_ids']:
                recommended_artists.add(artist_id)

    recommended_artists = sorted(recommended_artists, key=lambda x: [user_data['artist_ids'].index(x) for user_data in similar_users_data if x in user_data['artist_ids']][0])

    return recommended_artists

def create_recommended_playlist_for_user(cursor, data):
    user_id    = data['user_id']
    artist_ids = data['artist_ids']
    song_ids   = data['songs_ids']
    
    new_songs_ids = []
    for artist_id in artist_ids:
        artist_songs = get_songs_by_artist(cursor, artist_id)
        new_songs = [song for song in artist_songs if song not in song_ids]
        new_songs_ids += new_songs
        
    new_songs_ids = list(set(new_songs_ids))
    
    genre_to_songs = {}
    for song_id in new_songs_ids:
        song_genres = get_genres_by_song(cursor, song_id)
        if song_genres == None: continue
        for genre in song_genres:
            if genre not in genre_to_songs:
                genre_to_songs[genre] = []
            genre_to_songs[genre].append(song_id)
    
    playlists = []
    get_genre_name_by_id_query = """
        SELECT name
        FROM genres
        WHERE id=%s
    """
    for genre_id, songs_ids in genre_to_songs.items():
        cursor.execute(get_genre_name_by_id_query, (genre_id,))
        genre_name = cursor.fetchone()[0]
        playlist_data = {
            'name'        : f"Найкраще у жанрі {genre_name} для Вас",
            'description' : None,
            'cover'       : 1,
            'user_id'     : None,
            'for_user_id' : user_id
        }
        playlist_id = create_playlist(cursor, playlist_data)
        
        random.shuffle(songs_ids)
        length = min(len(songs_ids), 100)
        songs_ids = songs_ids[:length]
        
        playlist_songs_data = {
            'playlist_ids' : [playlist_id],
            'song_ids'     : songs_ids
        }
        add_songs_to_playlists(cursor, playlist_songs_data)

    get_new_playlists_query = """
        SELECT id
        FROM playlists
        WHERE for_user_id=%s
    """
    cursor.execute(get_new_playlists_query, (user_id,))
    new_playlist_ids = [row[0] for row in cursor.fetchall()]

    return new_playlist_ids

def create_user_best_mixes(cursor, user_id, user_songs_ids):
    genre_to_songs = {}
    for song_id in user_songs_ids:
        song_genres = get_genres_by_song(cursor, song_id)
        if song_genres is None: continue
        for genre in song_genres:
            if genre not in genre_to_songs:
                genre_to_songs[genre] = []
            genre_to_songs[genre].append(song_id)
    playlists = []
        
    get_genre_name_by_id_query = """
        SELECT name
        FROM genres
        WHERE id=%s
    """
    for genre_id, songs_ids in genre_to_songs.items():
        cursor.execute(get_genre_name_by_id_query, (genre_id,))
        genre_name = cursor.fetchone()[0]
        playlist_data = {
            'name'        : f"Твої найкращі мікси у жанрі {genre_name}",
            'description' : None,
            'cover'       : 1,
            'user_id'     : None,
            'for_user_id' : user_id
        }
        playlist_id = create_playlist(cursor, playlist_data)
        
        random.shuffle(songs_ids)
        length = min(len(songs_ids), 100)
        songs_ids = songs_ids[:length]
        
        playlist_songs_data = {
            'playlist_ids' : [playlist_id],
            'song_ids'     : songs_ids
        }
        add_songs_to_playlists(cursor, playlist_songs_data)

    get_new_playlists_query = """
        SELECT id
        FROM playlists
        WHERE for_user_id=%s
    """
    cursor.execute(get_new_playlists_query, (user_id,))
    new_playlist_ids = [row[0] for row in cursor.fetchall()]

    return new_playlist_ids
    
def delete_old_recommended_user_playlists(cursor, user_id):
    favourite_playlists_ids = get_playlists_from_favourite(cursor, user_id)
    get_playlist_ids_query = """
        SELECT id
        FROM playlists
        WHERE for_user_id=%s
    """
    
    cursor.execute(get_playlist_ids_query, (user_id,))
    rows = cursor.fetchall()
    playlist_ids_for_user = [row[0] for row in rows]
    
    for playlist_id in playlist_ids_for_user:
        if playlist_id not in favourite_playlists_ids:
            delete_playlist(cursor, playlist_id)
    return True

def reccomend_albums_by_artist(cursor, full_artist_ids, albums_ids):
    artist_count = Counter(full_artist_ids)
    sorted_artist_ids = [artist_id for artist_id, count in artist_count.most_common()]

    artist_albums = {}
    for artist_id in sorted_artist_ids:
        albums = get_albums_by_artist(cursor, artist_id)
        filtered_albums = [album_id for album_id in albums if album_id not in albums_ids] 
        if filtered_albums:
            artist_albums[artist_id] = filtered_albums

    return artist_albums

def reccomend_songs_by_artist(cursor, full_artist_ids, albums_ids):
    artist_albums = reccomend_albums_by_artist(cursor, full_artist_ids, albums_ids)
    song_ids = set()
    for album_id in artist_albums:
        song_ids.update(get_songs_by_album(cursor, album_id))
    return list(song_ids)

def recommend_categories_playlists(cursor, genres_ids):
    genre_count = Counter(genres_ids)
    sorted_unique_genres_ids = [genre for genre, count in genre_count.most_common()]
    
    number = min(len(sorted_unique_genres_ids), 3)
    sorted_unique_genres_ids = sorted_unique_genres_ids[:number]

    sorted_genres_names = tuple()
    for genre_id in sorted_unique_genres_ids:
        genre_name = get_genre_name_by_genre_id(cursor, genre_id)
        sorted_genres_names += (genre_name,)
        
    playlist_ids = set()

    placeholders = ', '.join(['%s'] * len(sorted_genres_names))
    get_id_playlist_by_tag_query = f"""
    SELECT id_playlist
    FROM playlist_tags
    WHERE tag IN ({placeholders})
    """

    cursor.execute(get_id_playlist_by_tag_query, sorted_genres_names)

    results = cursor.fetchall()
    for row in results:
        playlist_ids.add(row[0]) 

    return list(playlist_ids)

def create_basic_reccomendations(cursor):
    artists_ids  = get_most_popular_artists_overall(cursor, 15)
    albums_ids   = get_most_popular_albums_overall(cursor, 15)
    playlist_ids = get_most_popular_playlists_overall(cursor, 15)
    
    song_ids = set()
    for album_id in albums_ids:
        song_ids.update(get_songs_by_album(cursor, album_id))
    popular_songs = get_most_popular_songs(cursor, song_ids)
    
    songs_data = []
    for song_id in popular_songs:
        songs_data.append(get_song_info(cursor, song_id))
    artists_data = []
    for artist_id in artists_ids:
        artists_data.append(get_artist_info(cursor, artist_id))
    playlists_data = []
    for playlist_id in playlist_ids:
        playlist_data = get_playlist_info(cursor, playlist_id)
        if playlist_data['songs_count'] > 0:
            playlists_data.append(playlist_data)
    
    # random.shuffle(playlists_data)
    # random.shuffle(artists_data)
    # random.shuffle(songs_data)
    
    reccomendations = [
        {'type' : 'Playlist',   'title' : 'Варто послухати',     'data' : playlists_data},
        {'type' : 'Artist',     'title' : 'Популярні виконавці', 'data' : artists_data},
        {'type' : 'Song',       'title' : 'Топ крутих пісень',   'data' : songs_data},
    ]
    return reccomendations
    
def create_complex_reccomendations(cursor, user_id):
    return create_basic_reccomendations(cursor)

    main_user_data = get_user_tastes_data(cursor, user_id)

    if not main_user_data or not main_user_data['songs_ids']:
        return create_basic_reccomendations(cursor)
    #  ВИПРАВИТИ
    base = create_basic_reccomendations(cursor)

    reccomendations = []

    # reccomend artists
    recommended_artists = create_recommendations_OPTICS(cursor, main_user_data)
    create_recommended_playlist_data = {
        'user_id'    : user_id,
        'artist_ids' : recommended_artists,
        'songs_ids'  : main_user_data['songs_ids']
    }
    data  = recommended_artists
    title = 'Відкрийте для себе нових виконавців'
    if data: reccomendations.append({
        'type'  : 'Artist',
        'data'  : data,
        'title' : title
    })
    else: return base
    
    # create reccomend playlists
    data  = create_recommended_playlist_for_user(cursor, create_recommended_playlist_data)
    title = 'Спеціально для Вас'
    if data: reccomendations.append({
        'type'  : 'Playlist',
        'data'  : data,
        'title' : title
    })
    
    # reccomend albums
    data  = reccomend_songs_by_artist(cursor, main_user_data['full_artist_ids'], main_user_data['favourite_albums_ids'])
    title = 'Ці треки Вам точно сподобаються'
    if data: reccomendations.append({
        'type'  : 'Song',
        'data'  : data,
        'title' : title
    })

    #  create user best mixes
    data  = create_user_best_mixes(cursor, user_id, main_user_data['songs_ids'])
    title = 'Ваші найкращі мікси'
    if data: reccomendations.append({
        'type'  : 'Playlist',
        'data'  : data,
        'title' : title
    })
    
    # genre recomandations playlists
    data  = recommend_categories_playlists(cursor, main_user_data['genres_ids'])
    title = 'У Ваших улюблених жанрах'
    if data: reccomendations.append({
        'type'  : 'Playlist',
        'data'  : data,
        'title' : title
    })

    return base+reccomendations

#  ------------------------------------------------------------
def content_template(servername = "localhost", username = "root", password = "", database = "muzua"):
    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        result = None
        
        if conn.is_connected():

            cursor  = conn.cursor(buffered=True)
            
            result =  create_complex_reccomendations(cursor, "66521188002b9f819c8f")
            
            conn.commit()
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result


# success = content_template()
# print(
#     f"""
#     {success}
#     """
#     )

# f"""
#     user_id: {success['user_id']}
#     ------------------------------------
#     songs_ids: {success['songs_ids']}
#     ------------------------------------
#     artist_ids: {success['artist_ids']}
#     """