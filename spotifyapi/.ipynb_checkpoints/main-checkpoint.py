def template(data_function_dict, servername = "localhost", username = "root", password = "", database = "muzua"):
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
            
            for data_function in data_function_dict:
                for function in data_function['function']:
                    res = function(cursor, data_function['data'])
            conn.commit()
            cursor.close()

    except Error as e:
        print("Error:", e)
    finally:
        if conn.is_connected():
            conn.close()
            print("Connection closed")
            
data_function_dict = [
    {
        'data' :
        {
            'user_id' : 1,
            'music_ids' : [1, 2],
            'music_type' : 'playlist'
        },
        'function' : [delete_music_from_favourite]
    }
]
template(data_function_dict)


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
        'function' : [add_user]
    }
]
template(data_function_dict)
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
template(data_function_dict)
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
template(data_function_dict)
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
template(data_function_dict)
--------------------------------------------

--------------------------------------------
"""