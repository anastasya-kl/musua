import { View, Text, FlatList, Image, RefreshControl, Alert, Pressable, TouchableOpacity, TouchableWithoutFeedback, ScrollView } from 'react-native'
import React, { useEffect, useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'

import { icons, images } from '../../constants'
import SearchInput from '../components/SearchInput'
import Trending from '../components/Trending'
import EmptyState from '../components/EmptyState'
import SongCard from '../components/SongCard'
import { getAllPosts, getLatestPosts } from '../../lib/appwrite'
import useAppwrite from '../../lib/useAppwrite'
import PlaylistCard from '../components/PlaylistCard'
import PlaylistUserCard from '../components/PlaylistUserCard'
import { styled } from 'nativewind'
import dummyData from '../Mock/Dummy'
import FloatingPlayer from '../components/FloatingPlayer'
import FavoriteCard from '../components/FavoriteCard'
import { useGlobalContext } from '../../context/GlobalProvider';

const Library = ({ navigation }) => {
  const { data: posts, refetch } = useAppwrite(getAllPosts);
  const { data: latestPosts } = useAppwrite(getLatestPosts);

  const { user } = useGlobalContext();

  const [refreshing, setRefreshing] = useState(false);
  //const [selectedSong, setSelectedSong] = useState(null);

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch(); 
    setRefreshing(false);
  }

  return (
    <SafeAreaView className="bg-backg flex-1 h-full">
      <FlatList 
        ListHeaderComponent={() => (
          <View className="px-4">
          <View className="my-6 space-y-4">
            <View className="justify-between items-center flex-row">
                <View className="w-[50px] h-[50px] border border-blue rounded-[100px] items-center justify-center">
                  <Image 
                    source={{ uri: user?.avatar }}
                    className="w-[90%] h-[90%] rounded-[100px]"
                    resizeMode='cover'
                  />
                </View>
                <Text className="text-white font-medium text-[32px]">Медіатека</Text>
            </View>
          </View>

          <FavoriteCard />
          <PlaylistUserCard />

        </View>
        )}
      />
      <FloatingPlayer 
        title="Невідомо назви" 
        artist="Невідомий виконавець" 
        thumbnail={require('../../assets/images/unknown_track.png')}
      />
    </SafeAreaView>
  )
}

export default Library
