""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# --- IMPORT USER MODULES ---
from get_data import *


""" --- ADD NEW USER TO DATABASE ---
user_data structure:
'user_data':
    {
        'nickname'   : nickname,
        'password'   : password,
        'email'      : email,
        'birth_date' : birth_date
    }
--------------------------------"""
def add_user(cursor, data):
    nickname   = data['nickname']
    password   = data['password']
    email      = data['email']
    birth_date = data['birth_date']
    birth_date = convert_into_date(birth_date)
    
    insert_user_query = """
        INSERT INTO users (nickname, password, email, birth_date)
        VALUES (%s, %s, %s, %s)
    """
    values = (nickname, password, email, birth_date)
    try:
        cursor.execute(insert_user_query, values)
    except Error as e:
        print("Error:", e)
        

""" --- ADD SONGS, ALBUMS OR PLAYLISTS TO FAVOURITE ---
data structure:
'data':{
    'user_id' : user_id,
    'music_ids' : [music_id, music_id, ...],
    'music_type' : music_type }
music_type: 'song', 'album', 'playlist'
--------------------------------"""
def add_music_to_favourite(cursor, data):
    user_id    = data['user_id']
    music_ids  = data['music_ids']
    music_type = data['music_type']
    
    if music_type not in ['song', 'album', 'playlist']:
        raise ValueError("Incorrect music type")

    table = f"user_favourite_{music_type}s"
    
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM {table}
        WHERE id_user = %s AND id_{music_type} = %s
        );
    """
    insert_music_query = f"""
        INSERT INTO {table} (id_user, id_{music_type})
        VALUES (%s, %s)
    """
    for music_id in music_ids:
        values = (user_id, music_id)
        cursor.execute(check_query, values)
        if cursor.fetchone()[0] == 0:
            try: cursor.execute(insert_music_query, values)
            except Error as e: print("Error:", e)
        else:
            print("Data is already added")

            
""" --- DELETE SONGS, ALBUMS OR PLAYLISTS FROM FAVOURITE ---
data structure:
'data':{
    'user_id' : user_id,
    'music_ids' : [music_id, music_id, ...],
    'music_type' : music_type }
music_type: 'song', 'album', 'playlist'
--------------------------------"""
def delete_music_from_favourite(cursor, data):
    user_id    = data['user_id']
    music_ids  = data['music_ids']
    music_type = data['music_type']
    
    if music_type not in ['song', 'album', 'playlist']:
        raise ValueError("Incorrect music type")

    table = f"user_favourite_{music_type}s"
    
    delete_music_query = f"""
        DELETE FROM {table}
        WHERE id_user = %s AND id_{music_type} = %s
    """
    for music_id in music_ids:
        values = (user_id, music_id)
        cursor.execute(delete_music_query, values)
      
    
""" --- CREATE PLAYLIST ---
data structure:
'data':{
    'name' : name,
    'description' : description,
    'cover' : cover,
    'user_id' : user_id
    }
description AND cover can be none,true,false
user_id can be none/false if it is muzua playlist
--------------------------------"""
def create_playlist(cursor, data):
    name        = data['name']
    description = data['description']
    cover       = data['cover']
    user_id     = data['user_id']
    
    insert_playlist_query = f"""
        INSERT INTO playlists (name, description, cover, id_user)
        VALUES (%s, %s, %s, %s)
    """
    values = (name, description, cover, user_id)
    cursor.execute(insert_playlist_query, values)
    
    favourite_data = {
        'user_id'    : user_id,
        'music_ids'  : 1,
        'music_type' : 'playlist'
    }
    add_music_to_favourite(cursor, favourite_data)
    
    
""" --- UPDATE PLAYLIST DATA ---
data structure:
'data':{
    'playlist_id' : playlist_id
    'name' : name,
    'description' : description,
    'cover' : cover
    }
description AND cover can be null,true,false
--------------------------------"""
def update_user_playlist(cursor, data):
    playlist_id = data['playlist_id']
    name        = data['name']
    description = data['description']
    cover       = data['cover']
    
    update_playlist_query = f"""
        UPDATE user_playlists
        SET name = %s, description = %s, cover = %s
        WHERE id = %s
    """

    values = (name, description, cover, playlist_id)
    cursor.execute(update_playlist_query, values)
    
    
""" --- ADD SONGS TO PLAYLISTS ---
data structure:
'data':{
    'playlist_ids' : [playlist_id, playlist_id, ...]
    'song_ids' : [song_id, song_id, ...]
    }
    OR
'data':{
    'playlist_ids' : [playlist_id, playlist_id, ...]
    'song_ids' : [function, parameter, parameter, ...]
    }    
--------------------------------"""
def add_songs_to_playlists(cursor, data):
    playlist_ids = data['playlist_ids']
    if callable(data['song_ids'][0]):
        function = data['song_ids'][0]
        parametrs = [data['song_ids'][i] for i in range(1, len(data['song_ids']))]
        song_ids = function(cursor, *parametrs)
    else:
        song_ids =  data['song_ids']     
                     
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM user_playlist_songs
        WHERE id_playlist = %s AND id_song = %s
        );
    """
    add_song_to_playlist_query = f"""
        INSERT INTO user_playlist_songs (id_playlist, id_song)
        VALUES (%s, %s)
    """
    
    for playlist_id in playlist_ids:
        for song_id in song_ids:
            values = (playlist_id, song_id)
            cursor.execute(check_query, values)            
            if cursor.fetchone()[0] == 0:
                try: cursor.execute(add_song_to_playlist_query, values)
                except Error as e: print("Error:", e)
            else:
                print("Data is already added")
                
                
""" --- DELETE SONGS FROM PLAYLISTS ---
data structure:
'data':{
    'playlist_ids' : [playlist_id, playlist_id, ...]
    'song_ids' : [song_id, song_id, ...]
    }  
--------------------------------"""
def delete_songs_from_playlists(cursor, data):
    playlist_ids = data['playlist_ids']
    song_ids     =  data['song_ids']     
                     
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM user_playlist_songs
        WHERE id_playlist = %s AND id_song = %s
        );
    """
    delete_song_from_playlist_query = f"""
        DELETE FROM user_playlist_songs
        WHERE id_playlist = %s AND id_song = %s
    """
    
    for playlist_id in playlist_ids:
        for song_id in song_ids:
            values = (playlist_id, song_id)
            cursor.execute(delete_song_from_playlist_query, values)