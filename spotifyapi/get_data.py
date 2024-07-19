""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# --- IMPORT USER MODULES ---
from convert_data import *

""" --- GET SONGS FROM FAVOURITE ---
data structure:
user_id
--------------------------------"""
def get_songs_from_favourite(cursor, user_id):  

    get_songs_from_favourite_query = """
        SELECT id_song
        FROM user_favourite_songs
        WHERE id_user = %s
    """
    values = (user_id,)
    
    try:
        cursor.execute(get_songs_from_favourite_query, values)
        
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]

    except Error as e:
        return f"Error -> get_songs_from_favourite : {e}. Most likely user_id is incorrect"
            
    return song_ids

def get_songs_full_info_from_favourite(cursor, user_id):
    song_ids = get_songs_from_favourite(cursor, user_id)
    songs_full_info = []
    for song_id in song_ids:
        songs_full_info.append(get_song_info_for_user(cursor, song_id, user_id))

    return songs_full_info
    
""" --- GET ALBUMS FROM FAVOURITE ---
data structure:
user_id
--------------------------------"""
def get_albums_from_favourite(cursor, user_id):  
 
    get_albums_from_favourite_query = """
        SELECT id_album
        FROM user_favourite_albums
        WHERE id_user = %s
    """
    values = (user_id,)
    
    try:
        cursor.execute(get_albums_from_favourite_query, values)
        
        rows = cursor.fetchall()
        albums_ids = [row[0] for row in rows]

    except Error as e:
        return f"Error -> get_albums_from_favourite : {e}. Most likely user_id is incorrect"
            
    return albums_ids

""" --- GET PLAYLISTS FROM FAVOURITE ---
data structure:
user_id
--------------------------------"""
def get_playlists_from_favourite(cursor, user_id):  
 
    get_playlists_from_favourite_query = """
        SELECT id_playlist
        FROM user_favourite_playlists
        WHERE id_user = %s
    """
    values = (user_id,)
    
    try:
        cursor.execute(get_playlists_from_favourite_query, values)
        
        rows = cursor.fetchall()
        playlists_ids = [row[0] for row in rows]

    except Error as e:
        return f"Error -> get_albums_from_favourite : {e}. Most likely user_id is incorrect"
            
    return playlists_ids

def get_playlists_full_info_from_favourite(cursor, user_id, limit):
    if limit == 0:
        get_playlists_from_favourite_query = """
            SELECT id_playlist
            FROM user_favourite_playlists
            WHERE id_user = %s
            ORDER BY addition_date DESC
        """
        values = (user_id,)
    else:
        get_playlists_from_favourite_query = """
            SELECT id_playlist
            FROM user_favourite_playlists
            WHERE id_user = %s
            ORDER BY addition_date DESC
            LIMIT %s
        """
        values = (user_id, limit)
    
    cursor.execute(get_playlists_from_favourite_query, values)
    
    rows = cursor.fetchall()
    playlists_ids = [row[0] for row in rows]

    playlists_full_info = []
    get_addition_date_query = """
        SELECT addition_date
        FROM user_favourite_playlists
        WHERE id_playlist=%s AND id_user = %s
    """
    for playlist_id in playlists_ids:
        p_info = get_playlist_info(cursor, playlist_id)
        cursor.execute(get_addition_date_query, (playlist_id, user_id))
        addition_date = cursor.fetchone()[0]
        p_info['addition_date'] = addition_date
        playlists_full_info.append(p_info)

    return playlists_full_info


""" --- GET SONGS BY ALBUM ---
data structure:
album_id
--------------------------------"""
def get_songs_by_album(cursor, album_id):    
    get_songs_by_album_query = """
        SELECT id
        FROM songs
        WHERE id_album = %s
    """
    values = (album_id,)
    
    try:
        cursor.execute(get_songs_by_album_query, values)
        
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]

    except Error as e:
        return f"Error -> get_songs_by_album : {e}. Most likely album_id is incorrect"
            
    return song_ids

""" --- GET ALBUM BY SONGS ---
data structure:
song_id
--------------------------------"""
def get_album_by_song_id(cursor, song_id):    
    get_album_by_song_id_query = """
        SELECT id_album
        FROM songs
        WHERE id = %s
    """
    values = (song_id,)
    
    try:
        cursor.execute(get_album_by_song_id_query, values)
        
        album_id = cursor.fetchone()[0]

    except Error as e:
        return f"Error -> get_album_by_song_id : {e}. Most likely song_id is incorrect"
            
    return album_id
    
""" --- GET SONGS BY PLAYLIST ---
data structure:
playlist_id
--------------------------------"""
def get_songs_by_playlist(cursor, playlist_id):   
    playlist_id = int(playlist_id) 
    get_songs_by_playlist_query = """
        SELECT id_song
        FROM playlist_songs
        WHERE id_playlist = %s
    """
    values = (playlist_id,)
    
    try:
        cursor.execute(get_songs_by_playlist_query, values)
        
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]

    except Error as e:
        return f"Error -> get_songs_by_playlist : {e}. Most likely playlist_id is incorrect"
         
    return song_ids
    
""" --- GET SONGS BY ARTIST ---
data structure:
artist_id
--------------------------------"""
def get_songs_by_artist(cursor, artist_id):    
    get_songs_by_artist_query = """
        SELECT id_song
        FROM artist_songs
        WHERE id_artist = %s
    """
    values = (artist_id,)
    
    try:
        cursor.execute(get_songs_by_artist_query, values)
        
        rows = cursor.fetchall()
        song_ids = [row[0] for row in rows]
        
    except Error as e:
        return f"Error -> get_songs_by_artist : {e}. Most likely artist_id is incorrect"
    
    return song_ids

def songs_full_info_by_artist(cursor, artist_id):
    song_ids = list(set(get_songs_by_artist(cursor, artist_id)))
    songs_full_info = []
    for song_id in song_ids:
        songs_full_info.append(get_song_info(cursor, song_id))
    return songs_full_info

def songs_full_info_by_playlist(cursor, playlist_id, user_id):
    song_ids = list(set(get_songs_by_playlist(cursor, playlist_id)))
    songs_full_info = []
    for song_id in song_ids:
        songs_full_info.append(get_song_info_for_user(cursor, song_id, user_id))
    return songs_full_info


""" --- GET ALBUMS BY ARTIST ---
data structure:
artist_id
--------------------------------"""
def get_albums_by_artist(cursor, artist_id, album_type='album'):    
    get_albums_by_artist_query = """
        SELECT artist_albums.id_album
        FROM artist_albums
        JOIN albums ON artist_albums.id_album = albums.id
        WHERE artist_albums.id_artist = %s AND albums.type = %s
    """
    values = (artist_id, album_type)
    
    try:
        cursor.execute(get_albums_by_artist_query, values)
        
        rows = cursor.fetchall()
        album_ids = [row[0] for row in rows]
        
    except Error as e:
        return f"Error -> get_albums_by_artist : {e}. Most likely artist_id is incorrect"
    
    return list(set(album_ids))

""" --- GET ALBUM INFO ---
data structure:
album_id
--------------------------------"""
def get_album_info(cursor, album_id):
    get_album_info_query = """
        SELECT *
        FROM albums
        WHERE id = %s
    """
    result = {}
    values = (album_id,)
    try:
        cursor.execute(get_album_info_query, values)
        album_info = cursor.fetchone()
        
        result["id"]                 = album_info[0]
        result["name"]               = album_info[1]
        result["release_date"]       = album_info[2]
        result["album_total_tracks"] = album_info[3]
        result["background"]         = album_info[4]
        result["type"]               = album_info[5]
        
    except Error as e:
        return f"Error -> get_album_info : {e}. Most likely album_id is incorrect"
    
    return result

""" --- GET ARTIST INFO ---
data structure:
artist_id
--------------------------------"""
def get_artist_info(cursor, artist_id):
    get_artist_info_query = """
        SELECT *
        FROM artists
        WHERE id = %s
    """
    result = {}
    values = (artist_id,)
    try:
        cursor.execute(get_artist_info_query, values)
        artist_info = cursor.fetchone()
        
        result["id"]         = artist_info[0]
        result["name"]       = artist_info[1]
        result["popularity"] = artist_info[2]
        result["photo"]      = artist_info[3]
        
    except Error as e:
        return f"Error -> get_album_info : {e}. Most likely album_id is incorrect"

    return result
    
""" --- GET SONGS INFO ---
data structure:
playlist_id
--------------------------------"""
def get_song_info(cursor, song_id):
    get_song_info_query = """
        SELECT *
        FROM songs
        WHERE id = %s
    """
    get_artist_by_album_query = """
        SELECT id_artist
        FROM artist_albums
        WHERE id_album = %s
    """
    
    result = {
        "song"    : {},
        "album"   : {},
        "artists" : []
    }
    
    values = (song_id,)
    
    try:
        
        cursor.execute(get_song_info_query, values)
        song_info = cursor.fetchone()
    
        result["song"]["id"]             = song_info[0]
        result["song"]['name']           = song_info[1]
        result["song"]['duration_ms']    = song_info[2]
        result["song"]['track_number']   = song_info[3]
        result["song"]['preview_url_id'] = song_info[5]
        
        album_id        = song_info[4]
        result["album"] = get_album_info(cursor, album_id)
        
        values = (album_id,)
        cursor.execute(get_artist_by_album_query, values)
        rows = cursor.fetchall()
        artist_ids = [row[0] for row in rows]
                
        for artist_id in artist_ids: result["artists"].append(get_artist_info(cursor, artist_id))

    except Error as e: 
        return f"Error -> get_song_info : {e}. Most likely song_id is incorrect"
                    
    return result
        
def get_song_info_for_user(cursor, song_id, user_id):
    get_song_info_query = """
        SELECT *
        FROM songs
        WHERE id = %s
    """
    get_artist_by_album_query = """
        SELECT id_artist
        FROM artist_albums
        WHERE id_album = %s
    """
    
    result = {
        "song"    : {},
        "album"   : {},
        "artists" : []
    }
    
    values = (song_id,)
    
    try:
        result["isLiked"] = is_song_in_favourite(cursor, user_id, song_id)
        cursor.execute(get_song_info_query, values)
        song_info = cursor.fetchone()
    
        result["song"]["id"]             = song_info[0]
        result["song"]['name']           = song_info[1]
        result["song"]['duration_ms']    = song_info[2]
        result["song"]['track_number']   = song_info[3]
        result["song"]['preview_url_id'] = song_info[5]
        
        album_id        = song_info[4]
        result["album"] = get_album_info(cursor, album_id)
        
        values = (album_id,)
        cursor.execute(get_artist_by_album_query, values)
        rows = cursor.fetchall()
        artist_ids = [row[0] for row in rows]
                
        for artist_id in artist_ids: result["artists"].append(get_artist_info(cursor, artist_id))

    except Error as e: 
        return f"Error -> get_song_info : {e}. Most likely song_id is incorrect"
                    
    return result

""" --- GET PLAYLIST INFO ---
data structure:
playlist_id
--------------------------------"""
def get_playlist_info(cursor, playlist_id):
    playlist_id = int(playlist_id)
    get_playlist_info_query = """
        SELECT *
        FROM playlists
        WHERE id = %s
    """
    
    count_subscribers_query = """
        SELECT COUNT(*)
        FROM user_favourite_playlists
        WHERE id_playlist = %s
    """
    
    count_songs_query = """
        SELECT COUNT(*)
        FROM playlist_songs
        WHERE id_playlist = %s
    """
    
    get_background_query = """
        SELECT a.background
        FROM playlist_songs ps
        JOIN songs s ON ps.id_song = s.id
        JOIN albums a ON s.id_album = a.id
        WHERE ps.id_playlist = %s
        LIMIT 1
    """
    
    result = {}
    values = (playlist_id,)
    
    try:
        cursor.execute(get_playlist_info_query, values)
        playlist_info = cursor.fetchone()
        
        result['id']          = playlist_info[0]
        result['name']        = playlist_info[1]
        result['description'] = playlist_info[2]
        result['cover']       = playlist_info[3]
        result['id_user']     = playlist_info[4]
        
        # Підраховуємо кількість підписників плейлиста
        cursor.execute(count_subscribers_query, values)
        subscribers_count = cursor.fetchone()[0]
        result['subscribers_count'] = subscribers_count
        
        # Підраховуємо кількість пісень плейлиста
        cursor.execute(count_songs_query, values)
        songs_count = cursor.fetchone()[0]
        result['songs_count'] = songs_count

        # Вибрати обкладинку
        if songs_count == 0: result['background'] = False
        else:
            cursor.execute(get_background_query, values)
            background = cursor.fetchone()[0]
            result['background'] = background
        
    except Error as e:
        return f"Error -> get_playlist_info : {e}. Most likely playlist_id is incorrect"
           
    return result
    
    
""" --- GET ARTIST BY SONG_ID ---
data structure:
song_id
--------------------------------"""
def get_artist_by_song(cursor, song_id):
    album_id = get_album_by_song_id(cursor, song_id)
    get_artist_by_album_query = """
        SELECT id_artist
        FROM artist_albums
        WHERE id_album=%s
    """
    cursor.execute(get_artist_by_album_query, (album_id,))
    artist_id = cursor.fetchone()[0]
    
    return artist_id


""" --- GET GENRE NAME BY GENRE ID ---
data structure:
genre_id
--------------------------------"""
def get_genre_name_by_genre_id(cursor, genre_id):
    get_genre_name_by_genre_id_query = """
        SELECT name
        FROM genres
        WHERE id=%s
    """
    cursor.execute(get_genre_name_by_genre_id_query, (genre_id,))
    genre_name = cursor.fetchone()[0]
    
    return genre_name


def is_song_in_favourite(cursor, user_id, song_id):
    is_song_in_favourite_query = """
        SELECT EXISTS(
        SELECT 1
        FROM user_favourite_songs
        WHERE id_song = %s AND id_user = %s
    )
    """
    cursor.execute(is_song_in_favourite_query, (song_id, user_id))
    result = cursor.fetchone()
    return bool(result[0])

def is_playlist_in_favourite(cursor, user_id, playlist_id):
    is_playlist_in_favourite_query = """
        SELECT EXISTS(
        SELECT 1
        FROM user_favourite_playlists
        WHERE id_playlist = %s AND id_user = %s
    )
    """
    cursor.execute(is_playlist_in_favourite_query, (playlist_id, user_id))
    result = cursor.fetchone()
    return bool(result[0])

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
            
            result =  get_playlist_info(cursor, 6)
            
            conn.commit()
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result
    
# res = content_template()
# print(res)