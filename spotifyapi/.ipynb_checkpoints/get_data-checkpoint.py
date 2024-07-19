""" --- GET SONGS BY ALBUM ---
data structure:
'data':{
    'album_id' : album_id
    }
description AND cover can be null,true,false
--------------------------------"""
def get_songs_by_album(cursor, album_id):    
    get_songs_by_album_query = """
        SELECT id
        FROM songs
        WHERE id_album = %s
    """
    values = (album_id,)
    cursor.execute(get_songs_by_album_query, values)
    
    rows = cursor.fetchall()
    song_ids = [row[0] for row in rows]
    
    return song_ids