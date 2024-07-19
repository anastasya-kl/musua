import axios from 'axios';
import React, {useState, useEffect } from "react";
import { getAccount, getUserID } from "./appwrite";

export async function getFavouriteSongIds () {
    try {
      const userId = await getUserID();
      const response = await axios.get(`http://192.168.1.106:8080/api/songs_from_favourite/${userId}`);
      return(response.data)
    } catch (error) {
      console.error('Error fetching is liked:', error);
    }
  };

