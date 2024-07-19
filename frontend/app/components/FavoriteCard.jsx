import { View, Text, Image, TouchableWithoutFeedback, FlatList,RefreshControl, Pressable } from 'react-native'
import React, {useEffect, useState} from 'react'
import { icons } from '../../constants'
import axios from 'axios'
import { useRouter } from 'expo-router' 
import { getAccount, getUserID } from '../../lib/appwrite';
import {fetchSongFavourite, deleteSongFavourite, addSongFavourite, isSongLiked} from '../../lib/handleFavourite';

const FavoriteCard = ({}) => {
    const router = useRouter();
    
    const initializeLikedState = (favouriteData) => {
      const likedState = {};
      favouriteData.forEach((item) => {
        likedState[item.song.id] = item.isLiked;
      });
      return likedState;
    };
    
    const [favourite, setFavourite] = useState([]);
    const [refreshing, setRefreshing] = useState(false);
    const [isLiked, setIsLiked] = useState(() => initializeLikedState(favourite));
    
    useEffect(() => {
      const fetchData = async () => {
        const result = await fetchSongFavourite();
        setFavourite(result);
        setIsLiked(initializeLikedState(result));
      };
    
      fetchData();
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
          
          await addSongFavourite(songId);
        }
      } catch (error) {
        console.error('Error toggling favorite:', error);
      }
    };

    const handlePress = (item) => {
      router.push({
        pathname: `/player/${item.song.id}`,
        params: {
          dataContextData: "favourite"
        }
      });
    };

    const fetchFavoritesAndUpdateState = async () => {
      const result = await fetchSongFavourite();
      setFavourite(result);
      setIsLiked(initializeLikedState(result));
    };

    const onRefresh = async () => {
      setRefreshing(true);
      // await refetch();
      await fetchFavoritesAndUpdateState();
      // fetchRecommendations(userId);
      setRefreshing(false);
    };

    const _renderItem = ({ item, index }) => {
      const artists = item.artists.map((artist) => artist.name).join(', ');
      return (
        <Pressable onPress={() => handlePress(item)}>
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
        </Pressable>
      );
    };
    
    return (
      <View className="mb-[20px]">
        <View className="flex-row justify-between items-center">
            <Pressable onPress={onRefresh}>
              <Text className="text-gray-200 text-[16px] font-medium mt-[20px]" >Оновити</Text>
            </Pressable>      
        </View>
        <View className="flex-row justify-between items-center mt-[60px] mb-[30px]">
          <Text className="text-white text-[20px] font-medium">Уподобані</Text>
          <TouchableWithoutFeedback onPress={() => router.push(`/favorite/[favoriteId]`)}>
            <Image source={icons.arrowDown} className="w-[40px] h-[40px] rotate-180" />
          </TouchableWithoutFeedback>
        </View>
        <View>
          <FlatList
            keyExtractor={(item) => 'favorite_' + item.song.id}
            contentContainerStyle={{}}
            data={favourite}
            renderItem={_renderItem}
            refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
          />
        </View>
      </View>
    );
    return null
}

export default FavoriteCard