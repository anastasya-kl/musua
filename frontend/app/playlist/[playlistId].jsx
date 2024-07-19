import React, { useState, useEffect, useContext } from 'react';
import { View, Text, SafeAreaView, Image, TouchableOpacity, Alert, Pressable } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import dummyData from '../Mock/Dummy';
import PlaylistSong from '../components/PlaylistSong';
import { icons, images } from '../../constants';
import { PlaylistContext } from '../../context/PlaylistContext';
import axios from 'axios';
import CustomAlert from '../components/CustomAlert';
import { FetchFunctionsContext } from '../../context/FetchFunctionsContext';
import { getAccount, getUserID } from '../../lib/appwrite';
import {isPlaylistLiked, deletePlaylistFavourite, addPlaylistFavourite} from '../../lib/handleFavourite';

const Playlist = () => {  
  const router = useRouter();
  const { playlistId, playlistName, songsCount, playlistBackground, playlistUser} = useLocalSearchParams();
  // const currentUser = getUserId();
  // console.log(currentUser);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const fetchUserID = async () => {
      const userID = await getUserID();
      setCurrentUser(userID);
    };
    
    fetchUserID();
    }, []);

  // console.log(playlistId, playlistName, songsCount, playlistBackground)
  const { fetchPlaylistData, fetchReccData } = useContext(FetchFunctionsContext);
  const [isDeleted, setIsDeleted] = useState(false);
  const fetchDeletePlaylist = async () => {
    try {
      const response = await axios.get(`http://192.168.1.106:8080/api/delete/playlist/${playlistId}`);
      setIsDeleted(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const [isLiked, setIsLiked] = useState(null);
  useEffect(() => {
    const fetchIsLiked = async () => {
      const liked = await isPlaylistLiked(playlistId);
      setIsLiked(liked);
    };
    fetchIsLiked();
    }, []);
    console.log("isLiked", isLiked)
    console.log(playlistId)

  const toggleFavorite = async () => {
    try {
      const likedStatus = await isPlaylistLiked(playlistId);
      setIsLiked(!likedStatus);
      console.log("likedStatus ", likedStatus)
      if (likedStatus) {
        console.log("delete")
        await deletePlaylistFavourite(playlistId);
      } else {
        console.log("add")
        await addPlaylistFavourite(playlistId);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const [showAlert, setShowAlert] = useState(false);

  const getSongCountText = (count) => {
    if (count === 0) {
      return '0 пісень';
    } else if (count === 1) {
      return `${count} пісня`;
    } else if (count >= 2 && count <= 4) {
      return `${count} пісні`;
    } else {
      return `${count} пісень`;
    }
  };

  useEffect(() => {
    if (isDeleted) {
      router.back();
    }
  }, [isDeleted]);


  const handleBackPress = () => {
    router.back();
  };

  const handleMenuPress = () => {
    setShowAlert(true); // Показуємо алерт при натисканні на меню
  };

  const confirmDeletePlaylist = () => {
    Alert.alert('Підтвердження видалення', 'Чи дійсно ви бажаєте видалити плейлист?', [
      { text: 'Скасувати', style: 'cancel' },
      { text: 'Так', onPress: handleDeletePlaylist },
    ], { cancelable: false });
  };

  const handleDeletePlaylist = () => {
    fetchDeletePlaylist();
    setIsDeleted(true);
    // fetchPlaylistData(3);
    // fetchReccData();
  };

  // console.log(playlistUser, currentUser)
  return (
    <SafeAreaView className="bg-dark h-full mt-6">
      <View>
        <Image 
          source={  
            playlistBackground
              ? { uri: `https://i.scdn.co/image/${playlistBackground}` }
              : require('../../assets/images/unknown_track.png')
          }
          className="w-full h-[330px] mb-8 absolute"
          resizeMode='cover'
        />
        <View className="bg-black/60 w-full h-[330px] absolute"></View>

        <View className="flex-row justify-between items-center mx-4 mt-8">
          <TouchableOpacity onPress={handleBackPress} className="bg-black-100/60 rounded-[48px] items-center justify-center w-[46px] h-[46px]">
            <Image 
              source={icons.arrowDown}
              className="w-[90%] h-[90%]"
            />
          </TouchableOpacity>
          
          {playlistUser === currentUser && (
            <TouchableOpacity onPress={handleMenuPress} className="bg-black-100/60 rounded-[48px] items-center justify-center w-[46px] h-[46px]">
              <Image 
                source={require('../../assets/images/delete.png')}
                className="w-[80%] h-[80%]"
              />
            </TouchableOpacity>
          )}
          {playlistUser !== currentUser && (

            <TouchableOpacity onPress={() => toggleFavorite()} className="bg-black-100/60 rounded-[48px] items-center justify-center w-[46px] h-[46px]">
              {/* <Pressable onPress={toggleFavorite()}> */}
              <Image 
                source={isLiked ? icons.likeFill : icons.like}
                className="w-[65%] h-[65%]"
              />
              {/* </Pressable> */}
            </TouchableOpacity>
          )}
        </View>

        <Text className="text-white font-medium text-[32px] pl-8 pt-[140px]">{playlistName}</Text>
        <Text className="text-gray-200 font-regular text-[12px] pl-8 pt-[4px]">{getSongCountText(songsCount)}</Text>
      </View>
      <View className="px-4 mt-20">
        <PlaylistSong playlistId={playlistId} />
      </View>
      <CustomAlert // Викликаємо компонент CustomAlert
        visible={showAlert}
        onCancel={() => setShowAlert(false)}
        onConfirm={confirmDeletePlaylist}
      />
    </SafeAreaView>
  );
  return null
};

export default Playlist;
