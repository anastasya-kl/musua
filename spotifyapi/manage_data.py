""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random

# --- IMPORT USER MODULES ---
from convert_data import *
from content_data import *

""" -------- ADD SONGS, ALBUMS OR PLAYLISTS TO FAVOURITE --------
data structure:
'data':{
    'user_id' : user_id,
    'music_ids' : [music_id, music_id, ...],
    'music_type' : music_type }
music_type: 'song', 'album', 'playlist'
-----------------------------------------------------------"""
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
    
    try: 
        for music_id in music_ids:
            values = (user_id, music_id)
            cursor.execute(check_query, values)
            if cursor.fetchone()[0] == 0: cursor.execute(insert_music_query, values)
    except Error as e: 
        return f"Error -> add_music_to_favourite : {e}. Most likely music_ids and music_type have different types"
    
    return "Music is added"

def add_songs_to_favourite(cursor, user_id, song_id):
    
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM user_favourite_songs
        WHERE id_user = %s AND id_song = %s
        );
    """
    insert_song_query = f"""
        INSERT INTO user_favourite_songs (id_user, id_song)
        VALUES (%s, %s)
    """
    
    try:
        values = (user_id, song_id)
        cursor.execute(check_query, values)
        if cursor.fetchone()[0] == 0: cursor.execute(insert_song_query, values)
        else: return False
    except Error as e:
        return f"Error -> add_music_to_favourite : {e}"
    
    return True


def add_playlist_to_favourite(cursor, user_id, playlist_id):
    
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM user_favourite_playlists
        WHERE id_user = %s AND id_playlist = %s
        );
    """
    insert_playlist_query = f"""
        INSERT INTO user_favourite_playlists (id_user, id_playlist, addition_date)
        VALUES (%s, %s, %s)
    """
    
    try:
        addition_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(check_query, (user_id, playlist_id))
        if cursor.fetchone()[0] == 0: cursor.execute(insert_playlist_query, (user_id, playlist_id, addition_date))
        else: return False
    except Error as e:
        return f"Error -> add_playlist_to_favourite : {e}"
    
    return True
            
""" -------- DELETE SONGS, ALBUMS OR PLAYLISTS FROM FAVOURITE --------
data structure:
'data':{
    'user_id' : user_id,
    'music_ids' : [music_id, music_id, ...],
    'music_type' : music_type }
music_type: 'song', 'album', 'playlist'
-----------------------------------------------------------"""
def delete_music_from_favourite(cursor, data):
    user_id    = data['user_id']
    music_ids  = data['music_ids']
    music_type = data['music_type']
    
    if music_type not in ['song', 'album', 'playlist']:
        return f"{music_type} is incorrect type"

    table = f"user_favourite_{music_type}s"
    
    delete_music_query = f"""
        DELETE FROM {table}
        WHERE id_user = %s AND id_{music_type} = %s
    """
    
    try:
        for music_id in music_ids:
            values = (user_id, music_id)
            cursor.execute(delete_music_query, values)
    except Error as e:
        return f"Error -> delete_music_from_favourite : {e}"
    return {"Music is successfuly deleted"}

def delete_songs_from_favourite(cursor, song_id, user_id):
    
    delete_music_query = f"""
        DELETE FROM user_favourite_songs
        WHERE id_user = %s AND id_song = %s
    """
    
    try:
        values = (user_id, song_id)
        cursor.execute(delete_music_query, values)
    except Error as e:
        return f"Error -> delete_music_from_favourite : {e}"
    
    return True

def delete_playlist_from_favourite(cursor, playlist_id, user_id):
    
    delete_music_query = f"""
        DELETE FROM user_favourite_playlists
        WHERE id_user = %s AND id_playlist = %s
    """
    
    try:
        values = (user_id, playlist_id)
        cursor.execute(delete_music_query, values)
    except Error as e:
        return f"Error -> delete_music_from_favourite : {e}"
    
    return True
    
""" -------- CREATE PLAYLIST --------
data structure:
'data':{
    'name' : name,
    'description' : description,
    'cover' : cover,
    'user_id' : user_id,
    'for_user_id' : for_user_id
    }
description AND cover can be none,true,false
user_id can be none if it is muzua playlist
tags are separeted by ','
-----------------------------------------------------------"""
def create_playlist(cursor, data):
    name          = data['name']
    description   = data['description']
    cover         = data['cover']
    user_id       = data['user_id']
    for_user_id   = data['for_user_id']
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    insert_playlist_query = f"""
        INSERT INTO playlists (name, description, cover, id_user, creation_date, for_user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, description, cover, user_id, creation_date, for_user_id)
    
    try:
        cursor.execute(insert_playlist_query, values)
        playlist_id = cursor.lastrowid
        
        if user_id == None: return playlist_id
        
        favourite_data = {
            'user_id'    : user_id,
            'music_ids'  : [playlist_id],
            'music_type' : 'playlist'
        }
        add_music_to_favourite(cursor, favourite_data)
        return playlist_id
    
    except Error as e:
        return f"Error -> create_playlist : {e}"
    
    
""" -------- UPDATE PLAYLIST DATA --------
data structure:
'data':{
    'playlist_id' : playlist_id
    'name' : name,
    'description' : description,
    'cover' : cover
    }
None means to delete smth, False to not change anth
cover also can be True - change cover
-----------------------------------------------------------"""
def update_playlist(cursor, data):
    playlist_id = data['playlist_id']
    name        = data['name']
    description = data['description']
    cover       = data['cover']
    
    if name in [True, False] or playlist_id in [True, False, None]:
        return {"success" : False, "result" : "Data incorrect"}
    
    update_playlist_query = f"""
        UPDATE user_playlists
        SET 
    """
    values = tuple()
    
    if name: 
        update_playlist_query += """name = %s,"""
        values += (name,)
    if description == None: 
        update_playlist_query += """description = %s,"""
        values += (description,)
    if cover == None: 
        update_playlist_query += """cover = %s,"""
        values += (cover,)
    
    if not values:
        return "nothing to change"
    
    update_playlist_query = update_playlist_query[:-1]
    update_playlist_query += """WHERE id = %s"""

    values += (playlist_id,)
    
    try:
        cursor.execute(update_playlist_query, values)
    except Error as e:
        return f"Error -> update_user_playlist : {e}"
    
    return "Playlist is successfuly updated"
    
""" -------- ADD SONGS TO PLAYLISTS --------
data structure:
'data':{
    'playlist_ids' : [playlist_id, playlist_id, ...]
    'song_ids' : [song_id, song_id, ...]
    }
-----------------------------------------------------------"""
def add_songs_to_playlists(cursor, data):
    playlist_ids = data['playlist_ids']
    song_ids     = data['song_ids']
    insert_date  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
    check_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM playlist_songs
        WHERE id_playlist = %s AND id_song = %s
        );
    """
    add_song_to_playlist_query = f"""
        INSERT INTO playlist_songs (id_playlist, id_song, insert_date)
        VALUES (%s, %s, %s)
    """
    
    try: 
        for playlist_id in playlist_ids:
            for song_id in song_ids:
                cursor.execute(check_query, (playlist_id, song_id))            
                if cursor.fetchone()[0] == 0:
                    cursor.execute(add_song_to_playlist_query, (playlist_id, song_id, insert_date))
    except Error as e:
        return f"Error -> add_songs_to_playlists : {e}"
    
    return "Song is successfuly added"
                
                
""" -------- DELETE SONGS FROM PLAYLISTS --------
data structure:
'data':{
    'playlist_ids' : [playlist_id, playlist_id, ...]
    'song_ids' : [song_id, song_id, ...]
    }
-----------------------------------------------------------"""
def delete_songs_from_playlists(cursor, data):
    playlist_ids = data['playlist_ids']
    song_ids     =  data['song_ids']     
                     
    delete_song_from_playlist_query = f"""
        DELETE FROM playlist_songs
        WHERE id_playlist = %s AND id_song = %s
    """
    
    try:
        for playlist_id in playlist_ids:
            for song_id in song_ids:
                values = (playlist_id, song_id)
                cursor.execute(delete_song_from_playlist_query, values)
    except Error as e:
        return f"Error -> delete_songs_from_playlists : {e}"
    
    return "Song is successfuly deleted"

""" -------- ADD TAGS TO PLAYLIST --------
data structure:
'data':{
    'playlist_id' : playlist_id
    'tags' : ['tags names']
    }
-----------------------------------------------------------"""
def add_tags_to_playlist(cursor, data):
    playlist_id = data['playlist_id']
    tags        = data['tags']
    
    check_playlist_tag_query = f"""
        SELECT EXISTS (
        SELECT 1
        FROM playlist_tags
        WHERE id_playlist = %s AND tag = %s
        );
    """
    
    add_playlist_tag_query = f"""
        INSERT INTO playlist_tags (id_playlist, tag)
        VALUES (%s, %s)
    """
    
    try:
        for tag in tags:
            values = (playlist_id, tag)
            cursor.execute(check_playlist_tag_query, values)
            if cursor.fetchone()[0] == 0:
                cursor.execute(add_playlist_tag_query, values)
    except Error as e:
        return f"Error -> add_tags_to_playlist : {e}"
    
    return "tags are added"
        
            

""" -------- CLEAR PLAYLISTS --------
data structure:
    playlist_id
-----------------------------------------------------------"""
def clear_playlist(cursor, playlist_id):
    playlist_id = int(playlist_id)
    delete_playlist_songs_query = """
        DELETE FROM playlist_songs
        WHERE id_playlist = %s
    """
    delete_playlist_tags_query = """
        DELETE FROM playlist_tags
        WHERE id_playlist = %s
    """
    
    try:
        values = (playlist_id,)
        cursor.execute(delete_playlist_songs_query, values)
        cursor.execute(delete_playlist_tags_query, values)
    except Error as e:
        return f"Error -> clear_playlist : {e}"
    
    return f"Playlist is cleared"

""" -------- DELETE PLAYLISTS --------
data structure:
playlist_id
-----------------------------------------------------------"""
def delete_playlist(cursor, playlist_id):
    playlist_id = int(playlist_id)
    delete_playlist_from_favourite_for_all_users_query = f"""
        DELETE FROM user_favourite_playlists
        WHERE id_playlist = %s
    """
    
    delete_playlist_query = f"""
        DELETE FROM playlists
        WHERE id = %s
    """
    
    try:
        values = (playlist_id,)
        cursor.execute(delete_playlist_from_favourite_for_all_users_query, values)
        res = clear_playlist(cursor, playlist_id)
        cursor.execute(delete_playlist_query, values)
    except Error as e:
        return f"Error -> delete_playlists : {e}"
    
    return True

""" -------- CREATE PLAYLIST FOR CATEGORY --------
data = {
    'name' : name,
    'description' : description,
    'number' : number,
    'genre_restriction' : genre,
    'years_restriction' : []
}
"""

def create_playlist_for_category(cursor, data):
    
    try:
        playlist_data = {
            'name' : data['name'],
            'description' : data['description'],
            'cover' : 1,
            'user_id' : None
        }
        playlist_id = create_playlist(cursor, playlist_data)
        
        genre_restriction = data['genre_restriction']
        years_restriction = data['years_restriction']  
        get_subgenres_query = """
            SELECT name
            FROM genres
            WHERE name LIKE %s
        """
        genre_restriction_pattern = f'%{genre_restriction}%'
        cursor.execute(get_subgenres_query, (genre_restriction_pattern,))
        genres_restriction = [row[0] for row in cursor.fetchall()]
        
        tags = genres_restriction + years_restriction
        tags_data = {
            'playlist_id' : playlist_id,
            'tags'        : tags
        }
        add_tags_to_playlist(cursor, tags_data)
        
        song_ids_by_years  = get_songs_ids_by_years(cursor, years_restriction)
        song_ids_by_genres = get_songs_ids_by_genres(cursor, genres_restriction)
        song_ids = list(song_ids_by_years.intersection(song_ids_by_genres))
        song_ids = get_most_popular_songs(cursor, song_ids, data['number'])
        
        songs_data = {
            'playlist_ids' : [playlist_id],
            'song_ids'     : song_ids
        }
        add_songs_to_playlists(cursor, songs_data)
        return playlist_id
    
    except Error as e:
        return f"Error -> create_playlist_for_category : {e}"

def fill_categories_data(cursor):
    get_genres_names_query = """
        SELECT name
        FROM genres    
    """    
    cursor.execute(get_genres_names_query)
    genres_names = [row[0] for row in cursor.fetchall()]
    genres_names_placeholders = ','.join(['%s' for _ in genres_names])
    
    get_playlist_ids_query = """
        SELECT id_playlist
        FROM playlist_tags
    """
    cursor.execute(get_playlist_ids_query)
    playlist_ids = [row[0] for row in cursor.fetchall()]
    
    get_playlist_genres = f"""
        SELECT tag
        FROM playlist_tags
        WHERE tag IN ({genres_names_placeholders}) AND id_playlist = %s
    """
    
    playlists_with_genres = []
    
    # Виконуємо запит для кожного плейлиста
    for playlist_id in playlist_ids:
        cursor.execute(get_playlist_genres, genres_names + [playlist_id])
        genres = [row[0] for row in cursor.fetchall()]
        playlists_with_genres.append({'id': playlist_id, 'genres': genres})
        
    for data in playlists_with_genres:
        p_id   = data['id']
        genres = data['genres']
        songs_ids = get_songs_ids_by_genres(cursor, genres)
        number = min(len(songs_ids), 100)
        songs_ids = songs_ids[:number]
        add_songs_to_playlists(cursor, {
            'playlist_ids' : [p_id],
            'song_ids'     : songs_ids
        })
        
    return True

""" -------- CATEGORY ALL DATA -------- """
def category_all_data(cursor, category_genre_name):
    
    get_playlists = """
        SELECT id_playlist
        FROM playlist_tags
        WHERE tag LIKE %s
    """
    
    cursor.execute(get_playlists, (f"%{category_genre_name}%",))
    playlist_ids = [row[0] for row in set(cursor.fetchall())]
    
    album_ids  = get_most_popular_albums(cursor, get_albums_ids_by_genres(cursor, [category_genre_name]), 15)
    artist_ids = get_most_popular_artists(cursor, get_artists_ids_by_genres(cursor, [category_genre_name]), 15)
    
    category_data = {
        'playlist_ids' : playlist_ids,
        'album_ids'    : album_ids,
        'artist_ids'   : artist_ids
    }
    return category_data

def category_all_data_by_id(cursor, category_id):
    get_category_genre_by_id = """
        SELECT genre_name
        FROM categories
        WHERE id=%s
    """
    cursor.execute(get_category_genre_by_id, (category_id,))
    genre_name = cursor.fetchone()[0]
    category_data = category_all_data(cursor, genre_name)
    
    playlist_ids = category_data['playlist_ids']
    song_ids = set()
    for playlist_id in playlist_ids:
        song_ids.update(get_songs_by_playlist(cursor, playlist_id))
    
    song_ids = list(song_ids)
    number = min(len(song_ids), 60)
    song_ids = song_ids[:number]
    
    songs_full_data = []
    for song_id in song_ids:
        songs_full_data.append(get_song_info(cursor, song_id))
    
    get_category_name_by_id = """
        SELECT name
        FROM categories
        WHERE id=%s
    """
    cursor.execute(get_category_name_by_id, (category_id,))
    name = cursor.fetchone()[0]
    category_full_data = {
        'id'   : category_id,
        'name' : name,
        'data' : songs_full_data
    }
    return category_full_data

def get_all_categories_data(cursor):
    
    get_categories = """
        SELECT id, name, genre_name
        FROM categories
    """
    
    cursor.execute(get_categories)
    rows = cursor.fetchall()
    category_data = []
    for row in rows:
        category = {}
        category['id']         = row[0]
        category['name']       = row[1]
        category['genre_name'] = row[2]
        category['info']       = category_all_data(cursor, category['genre_name'])
        category_data.append(category)
    return category_data
    
def data_random_shuffle(some_data):
    for item in some_data:
        if 'data' in item:
            random.shuffle(item['data'])
    return some_data
    
# -------------------------------------------------------------
def manage_template(data, function, servername = "localhost", username = "root", password = "", database = "muzua"):
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
            
            result = add_playlist_to_favourite(cursor, "66521188002b9f819c8f",1307)
            # if data == None:
            #     result = function(cursor)
            # else:
            #     result = function(cursor, data)

            conn.commit()
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result
    

# result = manage_template(None, get_all_categories_data)
# print(result)
