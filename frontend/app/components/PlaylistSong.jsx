import { View, Text, Image, FlatList, Pressable } from 'react-native';
import React, {useState, useEffect} from 'react';
import dummyData from '../Mock/Dummy';
import { icons } from '../../constants';
import { getAccount, getUserID } from '../../lib/appwrite';
import axios from 'axios';
import {fetchSongsByPlaylist} from '../../lib/getSongs';

import {deleteSongFavourite, addSongFavourite, isSongLiked} from '../../lib/handleFavourite';

const PlaylistSong = ({ playlistId }) => {

  const initializeLikedState = (favouriteData) => {
    const likedState = {};
    favouriteData.forEach((item) => {
      likedState[item.song.isLiked] = true;
    });
    return likedState;
  };

  const [songs, setSongs] = useState([]);
  const [isLiked, setIsLiked] = useState(() => initializeLikedState(songs));

  const fetchSongs = async () => {
    try {
      const result = await fetchSongsByPlaylist(playlistId);
      setSongs(result);
      setIsLiked(initializeLikedState(result));
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };


  useEffect(() => {
    fetchSongs();
  }, []);

  const toggleFavorite = async (songId) => {
    try {
      const likedStatus = await isSongLiked(songId);
      setIsLiked((prevState) => ({
        ...prevState,
        [songId]: !likedStatus,
      }));
  
      if (likedStatus) {
        await deleteSongFavourite(songId);
      } else {
        // console.log("added");
        await addSongFavourite(songId);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  // useEffect(() => {
  //   songs.forEach((song) => {
  //     fetchIsLiked(song.song.id);
  //   });
  // }, [songs]);

  const _renderItem = ({ item, index }) => {
    const artists = item.artists.map((artist) => artist.name).join(', ');

    return (
      <View className="flex-row items-start justify-between mb-[16px]">
        <View className="flex-row items-center">
          <View>
            <Image
              key={index}
              source={{ uri: `https://i.scdn.co/image/${item.album.background}` }}
              className="w-[42px] h-[42px] rounded-[42px]"
            />
          </View>
          <View className="ml-[12px]">
            <Text className="font-medium text-white text-[14px]">{item.song.name}</Text>
            <Text className="font-medium text-gray-100 text-[12px] mt-[2px]">{artists}</Text>
          </View>
        </View>
          <Pressable onPress={() => toggleFavorite(item.song.id)}>
              <Image source={isLiked[item.song.id] ? icons.likeFill : icons.like} />
          </Pressable>
      </View>
    );
  };

  return (
    <Pressable>
      <View className="mb-[20px]">
        <View>
          <FlatList
            keyExtractor={(item) => 'playlistSong_' + item.song.id.toString()}
            contentContainerStyle={{}}
            data={songs}
            renderItem={_renderItem}
          />
        </View>
      </View>
    </Pressable>
  );
  return null
};

export default PlaylistSong;