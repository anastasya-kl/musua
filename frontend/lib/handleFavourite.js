import axios from 'axios';
import React, {useState, useEffect } from "react";
import { getAccount, getUserID } from "./appwrite";

export async function fetchSongFavourite() {
    try {
      const userId = await getUserID();
      console.log(userId);
      const response = await axios.get(`http://192.168.1.106:8080/api/songs_full_info_from_favourite/${userId}`);
    //   console.log(response.data);
      return(response.data);
    } catch (error) {
      console.error('Error fetching favourite:', error);
    }
  };

export async function deleteSongFavourite(songId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/delete_songs_from_favourite/${userId}/${songId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching favourite:', error);
    }
  };

export async function addSongFavourite(songId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/add_song_to_favourite/${userId}/${songId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching favourite:', error);
    }
  };

export async function isSongLiked (songId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/is_song_in_favourite/${userId}/${songId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching is liked:', error);
    }
  };

export async function fetchPlaylistFullInfoFavourite (limit){
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/playlists_full_info_from_favourite/${userId}/${limit}`);
      return(response.data);
    } catch (error) {
      console.error('Error fetching favourite:', error);
    }
  };

export async function createPlaylist(data) {
    try {
        const response = await axios.post('http://192.168.1.106:8080/api/create/playlist/', data);
        return response.data;
    } catch (error) {
        console.error('Error fetching favourite:', error);
    }
};

export async function isPlaylistLiked (playlistId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/is_playlist_in_favourite/${userId}/${playlistId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching is liked:', error);
    }
  };

export async function deletePlaylistFavourite (playlistId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/delete_playlist_from_favourite/${userId}/${playlistId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching deletePlaylistFavourite:', error);
    }
  };

export async function addPlaylistFavourite (playlistId) {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/add_playlist_to_favourite/${userId}/${playlistId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching addPlaylistFavourite:', error);
    }
  };



