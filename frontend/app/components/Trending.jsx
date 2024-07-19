import { View, Text, FlatList, TouchableOpacity, ImageBackground, Image } from 'react-native'
import React, { useState } from 'react'
import * as Animatable from 'react-native-animatable';
import { icons } from '../../constants';
import { useRouter } from 'expo-router';

const TrendingItem = ({ activeItem, item }) => {
  const [play, setPlay] = useState(false);

  const router = useRouter();

  const handlePress = (item) => {
    router.push({
      pathname: `/player/${item.id}`,
    });
  };

  return (
    <Animatable.View
      className="mr-[16px] mb-[20px]"
      duration={500}
    >
      <TouchableOpacity className="relative" activeOpacity={0.7} onPress={() => handlePress(item)}>
          <ImageBackground 
            source={{
              uri: item.thumbnail
            }}
            className="w-[132px] h-[132px] rounded-[4px] overflow-hidden"
            resizeMode='cover'
          />
          
          {/*<Image 
            source={icons.play}
            className="mt-[42px] ml-[42px] w-[48px] h-[48px] absolute"
            resizeMode='contain'
          />*/}

          <View className="w-[132px] mt-[10px]">
            <Text className="w-full text-white font-regular text-[14px] mb-[4px]">
              {item.title}
            </Text>
            <Text className="w-full text-gray-100 font-regular text-[12px]">
              {item.artist}
            </Text>
          </View>
      </TouchableOpacity>
      {/* {play ? (
        <Text className="text-white">Playing</Text>
      ) : (
        <TouchableOpacity className="relative" 
        activeOpacity={0.7} onPress={() => setPlay(true)}>
          <ImageBackground 
            source={{
              uri: item.thumbnail
            }}
            className="w-[132px] h-[132px] rounded-[4px] overflow-hidden"
            resizeMode='cover'
          />
          
          <Image 
            source={icons.play}
            className="mt-[42px] ml-[42px] w-[48px] h-[48px] absolute"
            resizeMode='contain'
          />

          <View className="w-[132px] mt-[10px]">
            <Text className="w-full text-white font-regular text-[14px] mb-[4px]">
              {item.title}
            </Text>
            <Text className="w-full text-gray-100 font-regular text-[12px]">
              {item.artist}
            </Text>
          </View>
      </TouchableOpacity>
      )} */}
    </Animatable.View>
  )
}

const Trending = ({ posts }) => {
  const [activeItem, setActiveItem] = useState(posts[0]);

  return (
    <FlatList 
        data={posts}
        horizontal
        keyExtractor={(item) => item.$id}
        renderItem={({ item }) => (
            <TrendingItem activeItem={activeItem} item={item} />
        )}
    />
  )
}

export default Trending;