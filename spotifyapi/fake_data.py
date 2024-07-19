""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime
# import tensorflow as tf
# from sklearn.cluster import DBSCAN
import pandas as pd
import string

# --- IMPORT USER MODULES ---
from user         import *
from get_data     import *
from order_data   import *
from manage_data  import *
from convert_data import *
from content_data import *
import random

def generate_random_user_id(length=20):
    characters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def get_random_data():
    names = ["Emily", "James", "Sophia", "Benjamin", "Olivia", "William", "Ava", "Alexander", "Charlotte", "Ethan"]
    
    number = random.randint(100000, 200000)
    name   = random.choice(names)
    return name + str(number)
    
def create_fake_users(cursor):
    nickname = get_random_data()
    email    = nickname + '@gamil.com'
    password = hash_password(nickname)
    user_id  = generate_random_user_id()

    check_user_id_query = """
        SELECT id 
        FROM users 
        WHERE id = %s
    """
    
    cursor.execute(check_user_id_query, (user_id,))

    exist = True if cursor.fetchone() else False
    while exist:
        user_id  = generate_random_user_id()
        cursor.execute(check_user_id_query, (user_id,))
        exist = True if cursor.fetchone() else False

    sign_up_user_account(cursor, {
        'user_id'  : user_id,
        'nickname' : nickname,
        'password' : password,
        'email'    : email
    })
    
    return user_id

def create_fake_playlist(cursor, user_id):

    get_all_genres_query = """
        SELECT name
        FROM genres
    """
    cursor.execute(get_all_genres_query)
    rows = cursor.fetchall()
    genres = [row[0] for row in rows]
    genres = [random.choice(genres)]

    if 'pop' in genres[0] or 'rock' in genres[0]:
        if 'pop' in genres[0]: genres = 'pop'
        else: genres = 'rock'
        
        get_all_genres_query = """
            SELECT name
            FROM genres
            WHERE name LIKE %s
        """
        cursor.execute(get_all_genres_query, (f"%{genres}%",))
        genres = [row[0] for row in cursor.fetchall()]
        
    song_ids = get_songs_ids_by_genres(cursor, genres)
    random.shuffle(song_ids)
    
    number   = min(random.randint(20,80), len(song_ids))+1
    song_ids = song_ids[:number]
    
    playlist_name = ", ".join(genres)
    playlist_id = create_playlist(cursor, {
        'name' : playlist_name,
        'description' : None,
        'cover' : 0,
        'user_id' : user_id,
        'for_user_id' : None
    })
    
    add_songs_to_playlists(cursor, {
        'playlist_ids' : [playlist_id],
        'song_ids' : song_ids
    })
    
    return genres


def add_random_albums(cursor, user_id, genres):
    albums_ids = get_albums_ids_by_genres(cursor, genres)
    random.shuffle(albums_ids)
    number = min(random.randint(3, 12), len(albums_ids))+1
    albums_ids = albums_ids[:number]
    add_music_to_favourite(cursor, {
        'user_id' : user_id,
        'music_ids' : albums_ids,
        'music_type' : 'album'
    })
    

def add_random_songs(cursor, user_id, genres):
    songs_ids = get_songs_ids_by_genres(cursor, genres)
    random.shuffle(songs_ids)
    number = min(random.randint(20,50), len(songs_ids))+1
    songs_ids = songs_ids[:number]
    add_music_to_favourite(cursor, {
        'user_id' : user_id,
        'music_ids' : songs_ids,
        'music_type' : 'song'
    })
    
    
def create_fake_data(cursor):
    user_id = create_fake_users(cursor)
    number = random.randint(3, 15)
    
    for n in range(number):
        genres = create_fake_playlist(cursor, user_id)
        # print("here")
    add_random_albums(cursor, user_id, genres)
    add_random_songs(cursor, user_id, genres)
    
    
def content_template(servername = "localhost", username = "root", password = "", database = "muzua"):
    # print("here")
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
            
            for user in range(30):
                create_fake_data(cursor)
                conn.commit()
                print(user+1, end=' ')
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result
    
# content_template()
# print(generate_random_user_id())