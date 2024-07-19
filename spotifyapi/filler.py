from dotenv import load_dotenv
import os
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret, sep='\n')

import base64
from requests import post
import json
from requests import get
import requests

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes  = auth_string.encode("utf-8")
    auth_base64 = str(base64.urlsafe_b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
    "Authorization" : "Basic " + auth_base64,
    "Content-Type"  : "application/x-www-form-urlencoded"
    }
    data = {
    "grant_type" : "client_credentials",
    "scope"      : "user-read-private user-read-email"  # Додайте потрібні області дії
    }
    result      = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token       = json_result["access_token"]
    return token;

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

artists_ids = []
with open("txt/artistsIds.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(":")
        artists_ids.append(parts[1].strip())
        
# print(artists_ids)

def get_artist_info(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    
    if 'error' in json_result:
        return False
            
    artist_name       = json_result['name']
    artist_popularity = json_result['popularity']
    artist_image      = json_result['images'][1]['url'][24:]
    artist_genres     = json_result['genres']
    artist_genres     = [genre.replace('ukrainian ', '') for genre in artist_genres]
    artist_genres     = [genre.replace('russian ', '') for genre in artist_genres]
    return {
        'artist_id'         : artist_id,
        'artist_name'       : artist_name,
        'artist_popularity' : artist_popularity,
        'artist_image'      : artist_image,
        'artist_genres'     : artist_genres
    }
    
"""token = get_token()
print(get_artist_info(token, artists_ids[0]))"""
    
def insert_artist(cursor, artist_data):
    artist_id  = artist_data['artist_id']
    name       = artist_data['artist_name']
    popularity = artist_data['artist_popularity']
    photo      = artist_data['artist_image']
    
    insert_artist_query = "INSERT INTO artists (id, name, popularity, photo) VALUES (%s, %s, %s, %s)"
    values = (artist_id, name, popularity, photo)
    cursor.execute(insert_artist_query, values)

def insert_genres(cursor, genres):            
    insert_genre_query = "INSERT INTO genres (name) VALUES (%s)"
    for genre in genres:
        try: cursor.execute(insert_genre_query, (genre,))
        except: continue

def insert_artist_genres(cursor, artist_id, genres):
    select_genre_ids_query = "SELECT id, name FROM genres"
    cursor.execute(select_genre_ids_query)
    genre_ids = {row[1]: row[0] for row in cursor.fetchall()}

    # Вставка зв'язків між артистом і жанрами в таблицю artist_genres
    for genre in genres:
        if genre in genre_ids:
            insert_artist_genre_query = "INSERT INTO artist_genres (id_artist, id_genre) VALUES (%s, %s)"
            values = (artist_id, genre_ids[genre])
            cursor.execute(insert_artist_genre_query, values)
    
import mysql.connector
from mysql.connector import Error

def fill_artists_info(artists_ids):
    servername = "localhost"
    username = "root"
    password = ""
    database = "muzua"

    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )

        if conn.is_connected():
            print("Connected successfully")

            cursor = conn.cursor()

            for artist_id in artists_ids:
                artist_info = get_artist_info(get_token(), artist_id)
                insert_artist(cursor, artist_info)
                insert_genres(cursor, artist_info['artist_genres'])
                insert_artist_genres(cursor, artist_info['artist_id'], artist_info['artist_genres'])

            conn.commit()
            cursor.close()

    except Error as e:
        print("Error:", e)
    finally:
        if conn.is_connected():
            conn.close()
            print("Connection closed")

def get_song_duration(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if 'error' in json_result:
        return False
        
    return json_result['duration_ms']

def update_duration_ms_for_all_songs():
    servername = "localhost"
    username = "root"
    password = ""
    database = "muzua"

    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        # Витягнути всі пісні з таблиці songs
        cursor.execute("SELECT id, duration_ms FROM songs")
        songs = cursor.fetchall()
        update_duration_ms_query = """
            UPDATE songs
            SET duration_ms = %s
            WHERE id = %s
        """
        for song in songs:
            song_id = song[0]
            if song[1] != 0: continue
            duration_ms = get_song_duration(get_token(), song_id)
            cursor.execute(update_duration_ms_query, (duration_ms, song_id))
            print(".", end =" ")
            conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(e)

# update_duration_ms_for_all_songs()

def get_song_popularity(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    if 'error' in json_result:
        return False
        
    return json_result['popularity']

def get_album_popularity(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if 'error' in json_result:
        raise Exception(json_result)
        
    return json_result['popularity']

def update_popularity_for_all_albums():
    servername = "localhost"
    username = "root"
    password = ""
    database = "muzua"

    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        # Витягнути всі пісні з таблиці songs
        cursor.execute("SELECT id, popularity FROM albums")
        albums = cursor.fetchall()
        update_popularity_query = """
            UPDATE albums
            SET popularity = %s
            WHERE id = %s
        """
        token = get_token()
        for album in albums:
            album_id = album[0]
            if album[1]: continue
            popularity = get_album_popularity(token, album_id)
            cursor.execute(update_popularity_query, (popularity, album_id))
            print(".", end =" ")
            conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(e)
        
update_popularity_for_all_albums()
# i = [j for j in range(2000,2025)]
# print(i)