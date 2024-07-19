# PYTHON MODULES
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from flask_cors import cross_origin
# USER MODULES
from user            import *
from get_data        import *
from order_data      import *
from manage_data     import *
from convert_data    import *
from content_data    import *
from recommendations import *

# CREATE APP
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']        = 'mysql://root:@localhost/muzua'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']    = False

db = SQLAlchemy(app)

""" --------------------  GET ENDPOINTS --------------------"""
#  GET FAVOURITE COMPONENTS

@app.route('/api/songs_from_favourite/<user_id>', methods=['GET'])
def get_songs_from_favourite_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_songs_from_favourite(cursor, user_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_full_info_from_favourite/<user_id>', methods=['GET'])
def get_songs_full_info_from_favourite_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_songs_full_info_from_favourite(cursor, user_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/albums_from_favourite/<user_id>', methods=['GET'])
def get_albums_from_favourite_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_albums_from_favourite(cursor, user_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/playlists_from_favourite/<user_id>', methods=['GET'])
def get_playlists_from_favourite_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_playlists_from_favourite(cursor, user_id)
    cursor.close()
    return jsonify(result)




#  GET SONGS BY <MUSIC COMPONENT>

@app.route('/api/album_by_song_id/<song_id>', methods=['GET'])
def get_album_by_song_id_endpoint(song_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_album_by_song_id(cursor, song_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_by_album/<album_id>', methods=['GET'])
def get_songs_by_album_endpoint(album_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_songs_by_album(cursor, album_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_by_playlist/<playlist_id>', methods=['GET'])
def get_songs_by_playlist_endpoint(playlist_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_songs_by_playlist(cursor, playlist_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_by_artist/<artist_id>', methods=['GET'])
def get_songs_by_artist_endpoint(artist_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_songs_by_artist(cursor, artist_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_full_info_by_artist/<artist_id>', methods=['GET'])
def get_songs_full_info_by_artist_endpoint(artist_id):
    cursor = db.engine.raw_connection().cursor()
    result = songs_full_info_by_artist(cursor, artist_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_full_info_by_playlist/<int:playlist_id>/<string:user_id>', methods=['GET'])
def get_songs_full_info_by_playlist_endpoint(playlist_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = songs_full_info_by_playlist(cursor, playlist_id, user_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/playlists_full_info_from_favourite/<string:user_id>/<int:limit>', methods=['GET'])
def get_playlists_full_info_from_favourite_endpoint(user_id, limit):
    cursor = db.engine.raw_connection().cursor()
    result = get_playlists_full_info_from_favourite(cursor, user_id, limit)
    cursor.close()
    return jsonify(result)

#  GET <MUSIC COMPONENT>

@app.route('/api/album/<album_id>', methods=['GET'])
def get_album_info_endpoint(album_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_album_info(cursor, album_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/artist/<artist_id>', methods=['GET'])
def get_artist_info_endpoint(artist_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_artist_info(cursor, artist_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/song/<string:song_id>', methods=['GET'])
def get_song_info_endpoint(song_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_song_info(cursor, song_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/song/<string:song_id>/<string:user_id>', methods=['GET'])
def get_song_info_for_user_endpoint(song_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_song_info_for_user(cursor, song_id, user_id)
    cursor.close()
    return jsonify(result)




@app.route('/api/playlist/<playlist_id>', methods=['GET'])
def get_playlist_info_endpoint(playlist_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_playlist_info(cursor, playlist_id)
    cursor.close()
    return jsonify(result)

# GET <MUSIC COMPONENT> BY

@app.route('/api/genres_by_artist/<artist_id>', methods=['GET'])
def get_genres_by_artist_endpoint(artist_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_genres_by_artist(cursor, artist_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/genres_by_song/<song_id>', methods=['GET'])
def get_genres_by_song_endpoint(song_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_genres_by_song(cursor, song_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_by_years/', methods=['POST'])
def get_songs_ids_by_years_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_songs_ids_by_years(cursor, data)
    cursor.close()
    return jsonify(result)

@app.route('/api/songs_by_genre/', methods=['POST'])
def get_songs_ids_by_genre_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_songs_ids_by_genres(cursor, data)
    cursor.close()
    return jsonify(result)

@app.route('/api/most_popular_songs/<number>', methods=['POST', 'GET'])
def get_most_popular_songs_endpoint(number):
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_most_popular_songs(cursor, data, number)
    cursor.close()
    return jsonify(result)

@app.route('/api/get_year_by_album/<album_id>', methods=['GET'])
def get_year_by_album_endpoint(album_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_year_by_album(cursor, album_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/get_albums_ids_by_years/', methods=['POST'])
def get_albums_ids_by_years_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_albums_ids_by_years(cursor, data)
    cursor.close()
    return jsonify(result)

@app.route('/api/albums_by_genres/', methods=['POST'])
def get_albums_ids_by_genres_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_albums_ids_by_genres(cursor, data)
    cursor.close()
    return jsonify(result)

@app.route('/api/most_popular_albums/<number>', methods=['POST', 'GET'])
def get_most_popular_albums_endpoint(number):
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = get_most_popular_albums(cursor, data, number)
    cursor.close()
    return jsonify(result)

@app.route('/api/most_popular_albums_overall/<number>', methods=['GET'])
def get_most_popular_albums_overall_endpoint(number):
    cursor = db.engine.raw_connection().cursor()
    result = get_most_popular_albums_overall(cursor, int(number))
    cursor.close()
    return jsonify(result)

@app.route('/api/category_all_data/<genre_name>', methods=['GET'])
def category_all_data_endpoint(genre_name):
    cursor = db.engine.raw_connection().cursor()
    result = category_all_data(cursor, genre_name)
    cursor.close()
    return jsonify(result)

@app.route('/api/get_all_categories_data/', methods=['GET'])
def get_all_categories_data_endpoint():
    cursor = db.engine.raw_connection().cursor()
    result = get_all_categories_data(cursor)
    cursor.close()
    return jsonify(result)

@app.route('/api/category_all_data_by_id/<int:cat_id>', methods=['GET'])
def get_category_all_data_by_id_endpoint(cat_id):
    cursor = db.engine.raw_connection().cursor()
    result = category_all_data_by_id(cursor, cat_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/artist_by_song/<song_id>', methods=['GET'])
def get_artist_by_song_endpoint(song_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_artist_by_song(cursor, song_id)
    cursor.close()
    return jsonify(result)

@app.route('/api/most_popular_artists_overall/<number>', methods=['GET'])
def get_most_popular_artists_overall_endpoint(number):
    cursor = db.engine.raw_connection().cursor()
    result = get_most_popular_artists_overall(cursor, int(number))
    cursor.close()
    return jsonify(result)

@app.route('/api/albums_by_artist/<album_id>', methods=['GET'])
def get_albums_by_artist_endpoint(album_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_albums_by_artist(cursor, album_id)
    cursor.close()
    return jsonify(result)


""" --------------------  POST ENDPOINTS --------------------"""

@app.route('/api/add/favourite/', methods=['POST'])
def add_music_to_favourite_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = add_music_to_favourite(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/add_song_to_favourite/<string:user_id>/<string:song_id>', methods=['GET'])
def add_song_to_favourite_endpoint(user_id, song_id):
    cursor = db.engine.raw_connection().cursor()
    result = add_songs_to_favourite(cursor, user_id, song_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/add_playlist_to_favourite/<string:user_id>/<int:playlist_id>', methods=['GET'])
def add_playlist_to_favourite_endpoint(user_id, playlist_id):
    cursor = db.engine.raw_connection().cursor()
    result = add_playlist_to_favourite(cursor, user_id, playlist_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)



@app.route('/api/delete/favourite/', methods=['POST'])
def delete_music_from_favourite_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = delete_music_from_favourite(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/delete_songs_from_favourite/<string:user_id>/<string:song_id>', methods=['GET'])
def delete_songs_from_favourite_endpoint(song_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = delete_songs_from_favourite(cursor, song_id, user_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/delete_playlist_from_favourite/<string:user_id>/<int:playlist_id>', methods=['GET'])
def delete_playlist_from_favourite_endpoint(playlist_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = delete_playlist_from_favourite(cursor, playlist_id, user_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)


@app.route('/api/is_song_in_favourite/<string:user_id>/<string:song_id>', methods=['GET'])
def is_song_in_favourite_endpoint(song_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = is_song_in_favourite(cursor, user_id, song_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/is_playlist_in_favourite/<string:user_id>/<int:playlist_id>', methods=['GET'])
def is_playlist_in_favourite_endpoint(playlist_id, user_id):
    cursor = db.engine.raw_connection().cursor()
    result = is_playlist_in_favourite(cursor, user_id, playlist_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/create/playlist/', methods=['POST'])
def create_playlist_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = create_playlist(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/update/playlist/', methods=['POST'])
def update_playlist_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = update_playlist(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/add/songs/to_playlists/', methods=['POST'])
def add_songs_to_playlists_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = add_songs_to_playlists(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/delete/songs/from_playlists/', methods=['POST'])
def delete_songs_from_playlists_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = delete_songs_from_playlists(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/add/tags/to_playlist/', methods=['POST'])
def add_tags_to_playlist_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = add_tags_to_playlist(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/clear/playlist/<int:playlist_id>', methods=['GET'])
def clear_playlist_endpoint(playlist_id):
    cursor = db.engine.raw_connection().cursor()
    result = clear_playlist(cursor, playlist_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/delete/playlist/<int:playlist_id>', methods=['GET'])
def delete_playlist_endpoint(playlist_id):
    cursor = db.engine.raw_connection().cursor()
    result = delete_playlist(cursor, playlist_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/create_playlist_for_category/', methods=['POST'])
def create_playlist_for_category_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = create_playlist_for_category(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

""" --------------------  USER ENDPOINTS --------------------"""

@app.route('/api/sign_up_user/', methods=['POST'])
def sign_up_user_account_endpoint():
    print("here")
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = sign_up_user_account(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/sign_in_user/', methods=['POST'])
def sign_in_user_account_endpoint():
    cursor = db.engine.raw_connection().cursor()
    data = request.get_json()
    result = sign_in_user_account(cursor, data)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/user_tastes/<user_id>', methods=['GET'])
def user_tastes_data_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = get_user_tastes_data(cursor, user_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)


""" --------------------  RECCOMENDATIONS --------------------"""
@app.route('/api/create_complex_reccomendations/<user_id>', methods=['GET'])
def create_complex_reccomendations_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = create_complex_reccomendations(cursor, user_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/delete_old_recommended_user_playlists/<user_id>', methods=['GET'])
def delete_old_recommended_user_playlists_endpoint(user_id):
    cursor = db.engine.raw_connection().cursor()
    result = delete_old_recommended_user_playlists(cursor, user_id)
    cursor.connection.commit()
    cursor.close()
    return jsonify(result)

@app.route('/api/data_random_shuffle/', methods=['POST'])
def data_random_shuffle_endpoint():
    data = request.get_json()
    result = data_random_shuffle(data)
    return jsonify(result)

""" --------------------  RUN APP --------------------"""
@app.route('/members', methods=['POST'])
def mambers():
    return {"members":["Member1","Member2","Member3"]}

@app.route('/check_connection', methods=['GET'])
def check_connection():
    return jsonify({'message': 'Server is running'}), 200

if __name__ == "__main__":
    app.run(debug=True)