""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# --- IMPORT USER MODULES ---
from get_data import *
from manage_data import *
from convert_data import *
from user import *

def write_logo_to_txt(logo, file_path = "logo.txt", rewrite_file = False):
    current_time = datetime.now()
    
    db_info = f"""
    --------------------> Date: {current_time} <--------------------
    Data base connection status       : {logo["connection"]}
    Data base commit status           : {logo["commit"]}
    Data base close connection status : {logo["close"]}
    Data base errors message          : {logo["DB error"]}
    Functions success feedbacks       : """
    for success in logo["functions success"]:
        db_info += f"\n\t\t\t{success}"
    db_info += """
    Functions results feedbacks       : """       
    for results in logo["functions results"]:
        db_info += f"\n\t\t\t{results}"    
    
    mode = 'w' if rewrite_file else 'a'
    with open(file_path, mode) as file:
        file.write(db_info)

def return_template(data_function, servername = "localhost", username = "root", password = "", database = "muzua"):
    logo = {
        "connection" : None, 
        "commit"     : None, 
        "close"      : None, 
        "DB error"   : None, 
        "functions success" : [], 
        "functions results" : []
        }
    results = None
    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )

        if conn.is_connected():
            logo["connection"] = True
            cursor  = conn.cursor()
            
            data     = data_function['data']
            function = data_function['function']

            results = function(cursor, data)
            
            logo["functions success"].append(results["success"])
            logo["functions results"].append(results["result"])
            
            conn.commit()
            cursor.close()
            
            logo["commit"] = True

    except Error as e:
        logo["DB error"] = e
    finally:
        if conn.is_connected():
            conn.close()
            logo["close"] = True
            write_logo_to_txt(logo=logo, rewrite_file=False)
            return results['result']
      

def execute_template(data_function_dict, servername = "localhost", username = "root", password = "", database = "muzua"):
    logo = {
        "connection" : None, 
        "commit"     : None, 
        "close"      : None, 
        "DB error"   : None, 
        "functions success" : [], 
        "functions results" : []
        }
    try:
        conn = mysql.connector.connect(
            host=servername,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )

        if conn.is_connected():
            logo["connection"] = True
            cursor  = conn.cursor()
            
            for data_function in data_function_dict:
                for function in data_function['function']:
                    f_res = function(cursor, data_function['data'])
                    logo["functions success"].append(f_res["success"])
                    logo["functions results"].append(f_res["result"])
            conn.commit()
            cursor.close()
            logo["commit"] = True

    except Error as e:
        logo["DB error"] = e
    finally:
        if conn.is_connected():
            conn.close()
            logo["close"] = True
            write_logo_to_txt(logo=logo, rewrite_file=False)
            

data_function_dict = [
    {
        'data':{
            "playlist_ids": [5],
            "song_ids": ["006WkdXOWZWnaCt092vIxK","00h9eif2nfiEA1ykBFLvBZ","00NjctUurkAaMz05EMdANN"]
        },
        'function' : [add_songs_to_playlists]
    }
]
execute_template(data_function_dict)

"""
--------------------------------------------
data_function_dict = [
    {
        'data':
        {
            'nickname'   : 'bona',
            'password'   : '2105',
            'email'      : 'ak@gmail.com',
            'birth_date' : '2004-05-21'
        },
        'function' : [sign_up_user_account]
    }
]
execute_template(data_function_dict)
--------------------------------------------
data_function_dict = [
    {
        'data' :
        {
            'user_id' : 1,
            'music_ids' : ['006WkdXOWZWnaCt092vIxK'],
            'music_type' : 'song'
        },
        'function' : [add_music_to_favourite]
    }
]
execute_template(data_function_dict)
--------------------------------------------
data_function_dict = [
    {
        'data':{
            'name' : 'relax',
            'description' : None,
            'cover' : False,
            'user_id' : 1
        },
        'function' : [create_playlist]
    }
]
--------------------------------------------
    {
        'data':{
            'playlist_id' : 1,
            'name' : "best relax",
            'description' : "best relax music",
            'cover' : False
        },
        'function' : [update_user_playlist]
    }
]
execute_template(data_function_dict)
--------------------------------------------
data_function_dict = [
    {
        'data':{
            'playlist_ids' : [1, 2],
            'song_ids' : ['0RM7XicQf5pdovlwdjaFDL', '2fKP3eayWmEO6UgtSijlGb']
        },
        'function' : [add_songs_to_playlists]
    },
    {
        'data':{
            'playlist_ids' : [1],
            'song_ids' : [get_songs_by_album, '01chilITc0rBjMWnCXQFLo']
        },
        'function' : [add_songs_to_playlists]
    }
]
execute_template(data_function_dict)
--------------------------------------------
data_function_dict = [
    {
        'data': [1],
        'function' : [delete_playlists]
    }
]
--------------------------------------------
"""