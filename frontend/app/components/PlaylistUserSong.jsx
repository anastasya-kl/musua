import { View, Text, Image, FlatList, Pressable } from 'react-native';
import React from 'react';
import dummyData from '../Mock/Dummy';
import { icons } from '../../constants';

const PlaylistUserSong = ({ playlistId }) => {

  const playlist = dummyData.Playlists.find(p => p.id === playlistId);

  if (!playlist) {
    return <Text>Playlist not found</Text>;
  }
  
  const filteredSongs = dummyData.Songs.filter(song => song.playlistname === playlist.name);

  const _renderItem = ({ item, index }) => {
    
    return (
      <View className="flex-row items-start justify-between mb-[16px]">
        <View className="flex-row items-center">
          <View>
            <Image
              key={index}
              source={item.thumbnail}
              className="w-[42px] h-[42px] rounded-[42px]"
            />
          </View>
          <View className="ml-[12px]">
            <Text className="font-medium text-white text-[14px]">{item.title}</Text>
            <Text className="font-medium text-gray-100 text-[12px] mt-[2px]">{item.artist}</Text>
          </View>
        </View>
        <Image source={icons.like} />
      </View>
    );
  };

  return (
    <Pressable>
      <View className="mb-[20px]">
        <View>
          <FlatList
            keyExtractor={item => 'playlistSong_' + item.id}
            contentContainerStyle={{}}
            data={filteredSongs}
            renderItem={_renderItem}
          />
        </View>
      </View>
    </Pressable>
  );
};

export default PlaylistUserSong;
