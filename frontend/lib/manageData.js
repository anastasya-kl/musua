import axios from 'axios';
import React, {useState, useEffect } from "react";
import {getUserID} from "./appwrite";
import { shuffle } from 'lodash';

export async function shuffleDataRandom(recommendations) {
    try {
        const response = await axios.post('http://192.168.1.106:8080/api/data_random_shuffle/', recommendations);
        return response.data;
    } catch (error) {
        console.error('Error fetching favourite:', error);
    }
};

export const shuffleData = (recommendations) => {
  const shuffledRecommendations = recommendations.map((item) => {
    const shuffledData = shuffle(item.data);
    return { ...item, data: shuffledData };
  });
  return shuffledRecommendations;
};