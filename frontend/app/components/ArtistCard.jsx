// components/ArtistCard.jsx

import { View, Text, Image, TouchableWithoutFeedback, FlatList } from 'react-native';
import React, {useState, useEffect} from 'react';
import { useRouter } from 'expo-router';
import dummyData from '../Mock/Dummy';
import { icons } from '../../constants';
import 'nativewind';
import axios from 'axios';

const ArtistCard = ({ data }) => {
  const router = useRouter();

  const _renderItem = ({ item, index }) => {
    const handlePress = () => {
      router.push({
        pathname: '/artist/[artistId]',
        params: {
          artistId: item.id,
          artistName: item.name,
          artistPhoto: item.photo,
        },
      });
    };
    return (
      <TouchableWithoutFeedback onPress={handlePress}>
        <View className="justify-center items-center">
          <View style={{ marginRight: index === data.length - 1 ? 0 : 16 }}>
            <Image
              key={index}
              source={{ uri: `https://i.scdn.co/image/${item.photo}` }}
              className="w-[150px] h-[150px] rounded-[150px]"
            />
            <Text className="w-[150px] text-white font-regular text-[14px] mt-[10px] text-center">
              {item.name}
            </Text>
          </View>
        </View>
      </TouchableWithoutFeedback>
    );
  };

  return (
    <View className="mb-[20px]">
      <View className="flex-row justify-between items-center" />
      <View>
        <FlatList
          keyExtractor={(item) => 'artist_' + item.id}
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{}}
          data={data}
          renderItem={_renderItem}
        />
      </View>
    </View>
  );
};

export default ArtistCard;

