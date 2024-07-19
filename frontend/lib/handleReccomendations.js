import axios from 'axios';
import React, {useState, useEffect } from "react";
import {getUserID} from "./appwrite";

export async function fetchRecommendations() {
    try {
      const userId = await getUserID()
      const response = await axios.get(`http://192.168.1.106:8080/api/create_complex_reccomendations/${userId}`);
      return(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };