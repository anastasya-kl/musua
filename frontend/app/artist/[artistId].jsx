// app/artist/[artistId].jsx

import { View, Text, SafeAreaView, Image, Button, TouchableOpacity } from 'react-native';
import React, {useEffect, useState} from 'react';
import 'nativewind';
import { useRouter, useLocalSearchParams } from 'expo-router';
import dummyData from '../Mock/Dummy';
import { icons, images } from '../../constants';
import ArtistSong from '../components/ArtistSong';
import axios from 'axios';

const Artist = () => {
  const { artistId, artistName, artistPhoto } = useLocalSearchParams();
  
  const router = useRouter();
  const [isSubscribed, setIsSubscribed] = useState(false);

  const handleSubscribePress = () => {
    setIsSubscribed(prevState => !prevState);
  }

  const handleBackPress = () => {
    router.back();
  }
  return (
    <SafeAreaView className="bg-backg h-full mt-6">
      <View>
        <Image 
          source={{ uri: `https://i.scdn.co/image/${artistPhoto}` }}
          className="w-full h-[280px] mb-8"
          resizeMode='cover'
        />
        <TouchableOpacity onPress={handleBackPress} className="bg-black-100/60 rounded-[48px] absolute items-center justify-center ml-4 mt-8 ">
          <Image 
            source={icons.arrowDown}
            className="w-[28px] h-[28px] px-6 py-6"
          />
        </TouchableOpacity>
        <View className="w-full items-center">
          <Text className="text-white items-center font-medium text-[32px]">{artistName}</Text>
        </View>

        <View className="px-4 mt-4 mb-[24px] flex-row justify-between items-start">
          <TouchableOpacity 
            activeOpacity={0.8} 
            onPress={handleSubscribePress} 
            className={`flex-row justify-center items-center w-[260px] h-[46px] ${isSubscribed ? 'bg-[#4779CB]' : 'bg-blue'} rounded-[4px]`}
          >
            <Text numberOfLines={1} ellipsizeMode="tail" className="font-regular text-black text-[18px]">{isSubscribed ? 'Ви підписані' : 'Підписатися'}</Text>
          </TouchableOpacity>

          <TouchableOpacity activeOpacity={0.5} className="flex-row justify-center items-center w-[46px] h-[46px] border-blue border-[1px] rounded-[4px]">
            <Image 
              source={icons.shuffle}
              className="w-[24px] h-[24px] mr-[4px]"
            />
          </TouchableOpacity>

        </View>
        <View className="px-4">
        <ArtistSong artistId={artistId} />
        </View>
      </View>
    </SafeAreaView>
  );
  return null
}

export default Artist;