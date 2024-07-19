import { View, Text, ImageBackground, TouchableOpacity, FlatList } from 'react-native';
import React from 'react';
import { useRouter } from 'expo-router';
import * as Animatable from 'react-native-animatable';

const SongCard = ({ data }) => {
  const router = useRouter();

  const handlePress = (item) => {
    router.push({
      pathname: `/player/${item.song.id}`
    });
  };

  const _renderItem = ({ item, index }) => {
    const artists = item.artists.map((artist) => artist.name).join(', ');

    return (
      <Animatable.View className="mr-[16px]" duration={500}>
        <TouchableOpacity className="relative" activeOpacity={0.7} onPress={() => handlePress(item)}>
          <ImageBackground
            key={index}
            source={{ uri: `https://i.scdn.co/image/${item.album.background}` }}
            className="w-[132px] h-[132px] rounded-[4px] overflow-hidden"
            resizeMode="cover"
          />
          <View className="w-[132px] mt-[10px]">
            <Text numberOfLines={1} ellipsizeMode="tail" className="w-full text-white font-regular text-[14px] mb-[4px]">
              {item.song.name}
            </Text>

            <Text numberOfLines={1} ellipsizeMode="tail" className="w-full text-gray-100 font-regular text-[12px]">
              {artists}
            </Text>
          </View>
        </TouchableOpacity>
      </Animatable.View>
    );
  };

  return (
    <FlatList
      keyExtractor={(item) => 'song_' + item.song.id}
      contentContainerStyle={{}}
      horizontal
      data={data}
      renderItem={_renderItem}
    />
  );
};

export default SongCard;