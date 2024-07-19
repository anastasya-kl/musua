import { View, Text, FlatList, Image, RefreshControl, Alert, Pressable, TouchableOpacity, ImageBackground } from 'react-native'
import React, { useEffect, useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'

import { images } from '../../constants'
import SearchInput from '../components/SearchInput'
import CategoryCard from '../components/CategoryCard'
import FloatingPlayer from '../components/FloatingPlayer'
import { useNavigation } from '@react-navigation/native'
import { useGlobalContext } from '../../context/GlobalProvider';

const Search = ({}) => {

  const { user } = useGlobalContext();

  const navigation = useNavigation();

  const handleCategoryClick = (categoryName) => {
    navigation.navigate('Category', { categoryName });
  };

  const [refreshing, setRefreshing] = useState(false)

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch(); 
    setRefreshing(false);
  }

  return (
    <SafeAreaView className="bg-backg h-full">
      <FlatList 
        ListHeaderComponent={() => (
          <View className="my-6 pl-4 space-y-6" >
            <View className="justify-between pr-4 items-center flex-row mb-4">
              <View className="w-[50px] h-[50px] border border-blue rounded-[100px] items-center justify-center">
                <Image 
                  source={{ uri: user?.avatar }}
                  className="w-[90%] h-[90%] rounded-[100px]"
                  resizeMode='cover'
                />
              </View>
              <Text className="text-white font-medium text-[32px]">Пошук</Text>
            </View>

            <View className="pr-4">
              <SearchInput />
            </View>

            <CategoryCard onPress={handleCategoryClick} />
            
          </View>
        )}
      />

      <FloatingPlayer></FloatingPlayer>
    </SafeAreaView>
  )
}

export default Search
