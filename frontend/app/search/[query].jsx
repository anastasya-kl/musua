import { View, Text, FlatList, Image, RefreshControl, Alert, Pressable } from 'react-native'
import React, { useEffect, useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'

import { images } from '../../constants'
import SearchInput from '../components/SearchInput'
import Trending from '../components/Trending'
import EmptyState from '../components/EmptyState'
import SongCard from '../components/SongCard'
import { getAllPosts, getLatestPosts, searchPosts } from '../../lib/appwrite'
import useAppwrite from '../../lib/useAppwrite'
import { useLocalSearchParams } from 'expo-router'

const Search = ({}) => {
  const { query } = useLocalSearchParams()
  const { data: posts, refetch } = useAppwrite(
    () => searchPosts(query)
  );

  console.log(query, posts)

  useEffect(() => {
    refetch();
  }, [query])

  return (
    <SafeAreaView className="bg-backg h-full">
      <FlatList
        
        ListHeaderComponent={() => (
          <View className="my-6 px-4">
            <Text className="font-regular text-sm text-gray-100">
              Пошук
            </Text>

            <Text className="text-2xl font-regular text-white">
              {query}
            </Text>

            <View className="mt-6 mb-8">
              <SearchInput initialQuery={query}  />
            </View>
            
          </View>
        )}
        
        ListEmptyComponent={() => (
          <EmptyState 
            title="Не знайдено пісні"
            subtitle="За цим пошуковим запитом не знайдено жодної пісні"
          />
        )}
      />
    </SafeAreaView>
  )
}

export default Search