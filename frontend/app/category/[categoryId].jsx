// app/category/[categoryId].jsx
import { View, Text, SafeAreaView, Image, TouchableOpacity } from 'react-native';
import 'nativewind';
import { useRouter, useLocalSearchParams } from 'expo-router';
import dummyData from '../Mock/Dummy'; 
import { icons } from '../../constants';
import FloatingPlayer from '../components/FloatingPlayer';
import React, { useEffect, useState } from 'react'
import CategorySong from '../components/CategorySong';
import axios from 'axios';

const Category = () => {
  category = useLocalSearchParams();
  const categoryId = category["categoryId"];

  const [categoryData, setCategoryData] = useState(null);
  const fetchCategoryData = async (categoryId) => {
    try {
      const response = await axios.get(`http://192.168.1.106:8080/api/category_all_data_by_id/${categoryId}`);
      setCategoryData(response.data);
    } catch (error) {
      console.error('Error fetching category data:', error);
    }
  };
  useEffect(() => {
    if (categoryId) {
      fetchCategoryData(categoryId);
    }
  }, [categoryId]);

  const router = useRouter();
  const handleBackPress = () => {
    router.back();
  }

  if (!categoryData) {
    return <Text>Loading...</Text>;
  }
  
  return (
    <SafeAreaView className="bg-backg h-full">
      <View>
        <View className="flex-row justify-between items-center mt-16 px-4">
          <TouchableOpacity
            onPress={handleBackPress}
            className="bg-black-100/60 rounded-[48px] items-center justify-center"
          >
            <Image source={icons.arrowDown} className="w-[28px] h-[28px] px-6 py-6" />
          </TouchableOpacity>
          <Text className="text-white font-medium text-right w-[240px] text-[32px]">{categoryData.name}</Text>
        </View>
        <View className="my-[28px] h-[1px] bg-gray-100/30"></View>
        <View>
          <CategorySong data={categoryData.data} />
        </View>
      </View>
    </SafeAreaView>
  );
  return null
}

export default Category;
