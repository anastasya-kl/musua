""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from get_data import *

""" --- SORT SONGS BY ...---
data structure:
songs_data list
--------------------------------"""
def sort_songs_by_duration_ms(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["song"]["duration_ms"], reverse=reverse)

def sort_songs_by_track_number(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["song"]["track_number"], reverse=reverse)

def sort_songs_by_name(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["song"]["name"], reverse=reverse)

def sort_songs_by_release_date(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["album"]["release_date"], reverse=reverse)

def sort_songs_by_album_name(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["album"]["name"], reverse=reverse)

def sort_songs_by_artist_name(songs_data, reverse=False):
    return sorted(songs_data, key=lambda x: x["artists"][0]["name"], reverse=reverse)

def sort_songs_by_popularity(songs_data, reverse=True):
    return sorted(songs_data, key=lambda x: x["song"]["popularity"], reverse=reverse)

def sort_song_ids_by_popularity(songs_data, reverse=True):
    return sorted(songs_data, key=lambda x: x["popularity"], reverse=reverse)