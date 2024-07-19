""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from collections import Counter

# USER MODULES
from get_data     import *
from order_data   import *
from manage_data  import *
from convert_data import *

""" ------------ GET ARTISTS BY ------------ """
def get_genres_by_artist(cursor, artist_id):
    
    get_genres_by_artist_query = """
        SELECT id_genre
        FROM artist_genres
        WHERE id_artist=%s
    """
    cursor.execute(get_genres_by_artist_query, (artist_id,))
    
    rows = cursor.fetchall()
    genres_ids = [row[0] for row in rows]
    
    if not genres_ids: return None
    return genres_ids

def get_artists_ids_by_genres(cursor, genres): 
    try: 
        genre_placeholders = ','.join(['%s' for _ in genres])
        get_genre_id_by_name_query = f"""
            SELECT id
            FROM genres
            WHERE name IN ({genre_placeholders})
        """
        cursor.execute(get_genre_id_by_name_query, genres)
        rows = cursor.fetchall()
        genre_ids = [row[0] for row in rows]
        if not genre_ids: return "genres names are invalid"
        
        
        genre_ids_placeholders = ','.join(['%s' for _ in genre_ids])
        get_artist_ids_by_genre_id_query = f"""
            SELECT id_artist
            FROM artist_genres
            WHERE id_genre IN ({genre_ids_placeholders})
        """
        cursor.execute(get_artist_ids_by_genre_id_query, genre_ids)
        rows = cursor.fetchall()
        artist_ids = [row[0] for row in rows]
    
        return artist_ids
    
    except Error as e:
        return f"Error -> get_artists_ids_by_genres : {e}"


def get_most_popular_artists(cursor, artist_ids, number=10):
    try:
        number = int(number)
        artist_ids_placeholders = ','.join(['%s' for _ in artist_ids])
        
        get_artist_id_popularity = f"""
            SELECT popularity
            FROM artists
            WHERE id IN ({artist_ids_placeholders})
        """
        
        cursor.execute(get_artist_id_popularity, artist_ids)
        rows = cursor.fetchall()
        artists_popularity = [0 if row[0] is None else row[0] for row in rows]
        
        artists_data = [{'artist_id': artist_id, 'popularity': popularity} for artist_id, popularity in zip(artist_ids, artists_popularity)]

        number = min(number, len(artists_data))
        artists_data = sort_song_ids_by_popularity(artists_data)[:number]
        artists_ids  = [item['artist_id'] for item in artists_data]
    
    except Error as e:
        return f"Error -> get_most_popular_albums : {e}"    
    
    return artists_ids

def get_most_popular_artists_overall(cursor, number):
    
    query = """
    SELECT id
    FROM artists
    ORDER BY popularity DESC
    LIMIT %s
    """
    
    cursor.execute(query, (number,))
    results = cursor.fetchall()
    
    artists_ids = [row[0] for row in results]
    
    return artists_ids

""" ------------ GET ALBUMS BY ------------ """
def get_year_by_album(cursor, album_id):
    
    get_year_by_album_query = """
        SELECT YEAR(release_date)
        FROM albums
        WHERE id=%s
    """
    cursor.execute(get_year_by_album_query, (album_id,))
    
    year = cursor.fetchone()[0]
    
    return year


def get_albums_ids_by_years(cursor, years):
    placeholders = ','.join(['%s' for _ in years])
    get_album_by_year_query = f"""
        SELECT id 
        FROM albums 
        WHERE YEAR(release_date) IN ({placeholders})
    """
    
    try:
        cursor.execute(get_album_by_year_query, years)
        rows = cursor.fetchall()
        album_ids = [row[0] for row in rows]
    except Error as e:
        return f"Error -> get_albums_ids_by_date : {e}"
    return album_ids


def get_albums_ids_by_genres(cursor, genres): 
    try: 
        genre_placeholders = ','.join(['%s' for _ in genres])
        get_genre_id_by_name_query = f"""
            SELECT id
            FROM genres
            WHERE name IN ({genre_placeholders})
        """
        cursor.execute(get_genre_id_by_name_query, genres)
        rows = cursor.fetchall()
        genre_ids = [row[0] for row in rows]
        if not genre_ids: return "genres names are invalid is invalid"
        
        
        genre_ids_placeholders = ','.join(['%s' for _ in genre_ids])
        get_artist_ids_by_genre_id_query = f"""
            SELECT id_artist
            FROM artist_genres
            WHERE id_genre IN ({genre_ids_placeholders})
        """
        cursor.execute(get_artist_ids_by_genre_id_query, genre_ids)
        rows = cursor.fetchall()
        artist_ids = [row[0] for row in rows]
        
        
        artist_ids_placeholders = ','.join(['%s' for _ in artist_ids])
        get_albums_ids_by_artist_id_query = f"""
            SELECT id_album
            FROM artist_albums
            WHERE id_artist IN ({artist_ids_placeholders})
        """
        cursor.execute(get_albums_ids_by_artist_id_query, artist_ids)
        rows = cursor.fetchall()
        albums_ids = [row[0] for row in rows]
    
        return albums_ids
    
    except Error as e:
        return f"Error -> get_albums_ids_by_genres : {e}"
                

def get_most_popular_albums(cursor, album_ids, number=10):
    try:
        number = int(number)
        album_ids_placeholders = ','.join(['%s' for _ in album_ids])
        
        get_album_id_popularity = f"""
            SELECT popularity
            FROM albums
            WHERE id IN ({album_ids_placeholders})
        """
        
        cursor.execute(get_album_id_popularity, album_ids)
        rows = cursor.fetchall()
        albums_popularity = [0 if row[0] is None else row[0] for row in rows]
        
        albums_data = [{'album_id': album_id, 'popularity': popularity} for album_id, popularity in zip(album_ids, albums_popularity)]

        number = min(number, len(albums_data))
        albums_data = sort_song_ids_by_popularity(albums_data)[:number]
        albums_ids  = [item['album_id'] for item in albums_data]
    
    except Error as e:
        return f"Error -> get_most_popular_albums : {e}"    
    
    return albums_ids

def get_most_popular_albums_overall(cursor, number):
    
    query = """
    SELECT id
    FROM albums
    ORDER BY popularity DESC
    LIMIT %s
    """
    
    cursor.execute(query, (number,))
    results = cursor.fetchall()
    
    album_ids = [row[0] for row in results]
    
    return album_ids
""" ------------ GET SONGS BY ------------ """

def get_genres_by_song(cursor, song_id):
    artist_id = get_artist_by_song(cursor, song_id)
    genres = get_genres_by_artist(cursor, artist_id)
    return genres

def get_songs_ids_by_years(cursor, years):
    
    try:
        album_ids = get_albums_ids_by_years(cursor, years)
        album_ids_placeholders = ','.join(['%s' for _ in album_ids])
        
        get_song_id = f"""
            SELECT id
            FROM songs
            WHERE id_album IN ({album_ids_placeholders})
        """
        
        cursor.execute(get_song_id, album_ids)
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]
        
        song_ids = []
        cursor.execute("SELECT id FROM songs")
        rows = cursor.fetchall()
        for row in rows: song_ids.append(row[0])
    except Error as e:
        return f"Error -> get_songs_ids_by_date : {e}"
    
    return list(set(song_ids))


def get_songs_ids_by_genres(cursor, genres):
    
    try:
        album_ids = get_albums_ids_by_genres(cursor, genres)
        album_ids_placeholders = ','.join(['%s' for _ in album_ids])
        
        get_song_id = f"""
            SELECT id
            FROM songs
            WHERE id_album IN ({album_ids_placeholders})
        """
        
        cursor.execute(get_song_id, album_ids)
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]
        
        song_ids = []
        cursor.execute("SELECT id FROM songs")
        rows = cursor.fetchall()
        for row in rows: song_ids.append(row[0])
    except Error as e:
        return f"Error -> get_songs_ids_by_genre : {e}"
    
    return list(set(song_ids))


def get_most_popular_songs(cursor, song_ids, number=50):
    
    number = int(number)
    
    get_song_id_popularity = """
        SELECT popularity
        FROM songs
        WHERE id=%s
    """
    songs_data = []
    
    for song_id in song_ids:
        cursor.execute(get_song_id_popularity, (song_id,))
        popularity = cursor.fetchone()[0]
        if popularity is None: popularity = 0
        songs_data.append({
            "song_id"    : song_id,
            "popularity" : popularity
        })

    number = min(number, len(songs_data))
    songs_data = sort_song_ids_by_popularity(songs_data)[:number]
    
    song_ids = [item['song_id'] for item in songs_data]
    return list(set(song_ids))

        
""" ------------ GET PLAYLISTS BY ------------ """
def get_most_popular_playlists_overall(cursor, number):
    get_all_playlists_query = """
        SELECT id_playlist
        FROM user_favourite_playlists
    """
    cursor.execute(get_all_playlists_query)
    rows = cursor.fetchall()
    
    playlist_ids = [row[0] for row in rows]
    playlist_counter = Counter(playlist_ids)

    sorted_playlists = [playlist for playlist, count in playlist_counter.most_common()]
    number = min(len(sorted_playlists), number)
    sorted_playlists = sorted_playlists[:number]
    
    return sorted_playlists

def content_template(data, function, servername = "localhost", username = "root", password = "", database = "muzua"):
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

            cursor  = conn.cursor()
            
            result = function(cursor, data)

            conn.commit()
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result


# result = content_template("0896FugzPOpBDwYEfhMAVY", get_genres_by_artist)
# print(result)