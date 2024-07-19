""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# --- IMPORT USER MODULES ---
from user            import *
from get_data        import *
from order_data      import *
from manage_data     import *
from convert_data    import *
from content_data    import *
from recommendations import *

""" -------- ADD NEW USER TO DATABASE --------
data structure:
'data':
    {
        'user_id'  : user_id,
        'nickname' : nickname,
        'password' : password,
        'email'    : email
    }
-----------------------------------------------------------"""
def sign_up_user_account(cursor, data):
    user_id  = data['user_id']
    nickname = data['nickname']
    password = data['password']
    email    = data['email']
    
    password = hash_password(password)
    
    insert_user_query = """
        INSERT INTO users (id, nickname, password, email)
        VALUES (%s, %s, %s, %s)
    """
    values = (user_id, nickname, password, email)
    try:
        cursor.execute(insert_user_query, values)
        
        user_info = {
            "user_id"    : user_id,
            "nickname"   : nickname,
            "email"      : email
        }
        
        return user_info
    
    except Error as e:
        return f"Error -> sign_up_user_account: {e}. Most likely the user already exists"


""" -------- GET FULL USER INFO --------
data structure:
'data':
    {
        'password' : password,
        'email'    : email
    }
--------------------------------"""
def sign_in_user_account(cursor, data):
    password = data['password']
    email    = data['email']
    
    password = hash_password(password)
    
    user_info_query = """SELECT id, nickname, email
        FROM users
        WHERE email = %s AND password = %s 
    """
    values = (email, password)
    
    try:
        cursor.execute(user_info_query, values)
        row = cursor.fetchone()
        
        user_info = {}
        if row:
            user_info['user_id']    = row[0]
            user_info['nickname']   = row[1]
            user_info['email']      = row[2]
        return user_info
    except Error as e:
        return f"Error: -> sign_in_user_account : {e}. Most likely user doesn't exist"
    
  
""" -------- DELETE USER --------
data structure:
user_id
--------------------------------"""
def delete_user_account(cursor, user_id):
    try:
        song_ids     = get_songs_from_favourite(cursor, user_id)
        album_ids    = get_albums_from_favourite(cursor, user_id)
        playlist_ids = get_playlists_from_favourite(cursor, user_id)
        
        delete_music_from_favourite(cursor, {
            'user_id' : user_id,
            'music_ids' : song_ids,
            'music_type' : 'song'
        })
        
        delete_music_from_favourite(cursor, {
            'user_id' : user_id,
            'music_ids' : album_ids,
            'music_type' : 'album'
        })
        
        for playlist_id in playlist_ids:
            delete_playlist(cursor, playlist_id)
            
        delete_user_query = """
            DELETE FROM users
            WHERE id=%s
        """
        cursor.execute(delete_user_query, (user_id,))
        
        return True
    except Error as e:
        return f"Error -> sign_in_user_account : {e}"
    
def remove_all_users(cursor, conn):
    
    get_all_user_ids = """
        SELECT id
        FROM users
    """
    
    cursor.execute(get_all_user_ids)
    rows = cursor.fetchall()
    user_ids = [row[0] for row in rows]
    
    for user_id in user_ids:
        delete_user_account(cursor, user_id)
        conn.commit()
        print('. ', end='')
        
    return True

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
            
            if data == None: result = function(cursor, conn)
            else: result = function(cursor, data)

            conn.commit()
            cursor.close()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
        return result
    
    
# data = {
#     "user_id" : "6651fa3300154f51f5e1",
#     "nickname" : "rock_2024",
#     "password" : "password",
#     "email" : "email@gmail.com"
# }
# print(len(data['user_id']))

# res = manage_template(data, sign_up_user_account)
# print(res)