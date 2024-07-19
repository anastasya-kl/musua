import { View, Text, FlatList, Image,TouchableOpacity, Pressable } from 'react-native'
import React, {useState, useEffect} from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { useNavigation } from '@react-navigation/native'
import dummyData from '../Mock/Dummy'
import { icons } from '../../constants'
import { useRouter } from 'expo-router';
import { useLocalSearchParams } from 'expo-router';
import {fetchSongFavourite, deleteSongFavourite, addSongFavourite, isSongLiked} from '../../lib/handleFavourite';

const FavoriteScreen = () => {
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
      const artists = item.artists.map((artist) => artist.name).join(', ');
      console.log("Navigating to player screen with item", item);
      router.push({
          pathname: '/player',
          params: { 
              title: item.song.name, 
              artist: artists,
              thumbnail: item.album.background 
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

  const handleBackPress = () => {
    router.back();
  };

  // console.log(favourite);
  const _renderItem = ({ item, index }) => {
    const artists = item.artists.map((artist) => artist.name).join(', ');
    return (
      <View className="flex-row items-start justify-between mb-[16px]" >

        <View className="flex-row items-center">
          <View>
            <Image 
              key={ index }
              source={{ uri: `https://i.scdn.co/image/${item.album.background}`}}
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
    )
  }

  return (
    <SafeAreaView className="bg-backg flex-1 h-full px-4 pb-16">
      <View className="my-6 space-y-4">
        <View className="flex-row justify-between">
          <TouchableOpacity onPress={handleBackPress}>
            <Image 
              source={icons.arrowDown}
              className="w-[42px] h-[42px] mt-[4px]"
            />
          </TouchableOpacity>
          <Text className="text-white font-medium text-[32px] mb-6">Уподобані</Text>
        </View>
        <View className="flex-row justify-between items-center">
            <Pressable onPress={onRefresh}>
              <Text className="text-gray-200 text-[16px] font-medium mt-[20px]" >Оновити</Text>
            </Pressable>      
        </View>
        <FlatList 
          keyExtractor={(item) => 'favorite_' + item.id}
          data={favourite}
          renderItem={_renderItem}
        />
      </View>
    </SafeAreaView>
  )
}

export default FavoriteScreen
