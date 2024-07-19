""" --- IMPORTING --- """
# --- IMPORT LIBRARIES ---
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# --- IMPORT USER MODULES ---
from convert_data import *

""" --- GET FULL  ---
data structure:
'data':{
    'album_id' : album_id
    }
--------------------------------"""