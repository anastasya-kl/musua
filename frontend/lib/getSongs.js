import axios from 'axios';
import React, {useState, useEffect } from "react";
import {getUserID} from "./appwrite";

export async function fetchSongsByPlaylist(playlistId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/songs_full_info_by_playlist/${playlistId}/${userId}`);
      return(response.data);
    } catch (error) {
      console.error('Error fetching fetchSongsByPlaylist:', error);
    }
  };

export async function fetchSongInfo(songId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/song/${songId}/${userId}`);
      return(response.data);
    } catch (error) {
      console.error('Error fetching fetchSongsInfo:', error);
    }
  };