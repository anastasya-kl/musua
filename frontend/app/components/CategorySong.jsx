import { View, Text, Image, FlatList, Pressable } from 'react-native';
import React from 'react';
import dummyData from '../Mock/Dummy';
import { icons } from '../../constants';

const CategorySong = ({ data }) => {

  const _renderItem = ({ index, item  }) => {

    const artists = item.artists.map((artist) => artist.name).join(', ');

    return (
      <View className="flex-row justify-between mb-[20px]">
        <View>
          <Image 
            key={index}
            source={{ uri: `https://i.scdn.co/image/${item.album.background}` }}
            className="w-[120px] h-[120px] rounded-[4px] mb-[8px] mr-[10px]"
          />
          <Text numberOfLines={1} ellipsizeMode="tail" className="font-medium w-[100px] text-white text-[14px]">{item.song.name}</Text>
          <Text numberOfLines={1} ellipsizeMode="tail" className="font-medium w-[100px] text-gray-100 text-[12px] mt-[2px]">{artists}</Text>
        </View>
      </View>
    );
  };

  return (
    <Pressable>
      <View className="mb-[20px] mx-4">
        <FlatList
          keyExtractor={(item) => 'song_' + item.song.id}
          numColumns={3}
          data={data}
          renderItem={_renderItem}
        />
      </View>
    </Pressable>
  );
};

export default CategorySong;
