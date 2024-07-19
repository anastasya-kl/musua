import { View, Text, Image, TouchableWithoutFeedback, FlatList, TouchableOpacity, TextInput, Modal, Button } from 'react-native'
import React, { useContext, useEffect, useState } from 'react';
import { icons } from '../../constants'
import dummyData from '../Mock/Dummy'
import { useRouter } from 'expo-router';
import { PlaylistContext } from '../../context/PlaylistContext';


const PlaylistCard = ({ data }) => {
  const router = useRouter();


  const _renderItem = ({ item, index }) => {
    const handlePress = () => {
      router.push({
        pathname: '/playlist/[playlistId]',
        params: {       
          playlistId: item.id,
          playlistName: item.name,
          songsCount: item.songs_count,
          playlistBackground: item.background,
          playlistUser: item.id_user
        }
      });
    };
    return (
      <TouchableWithoutFeedback onPress={handlePress}>
        <View style={{ marginRight: index === data.length - 1 ? 0 : 16 }}>
          <Image
            key={index}
            source={{ uri: `https://i.scdn.co/image/${item.background}` }}
            className="w-[150px] h-[150px] rounded-[4px]"
          />
          <Text className="w-full text-white font-regular text-[14px] mb-[4px] mt-[10px]">
            {item.name.length > 22 ? `${item.name.slice(0, 22)}...` : item.name}
          </Text>
          <Text className="w-full text-gray-100 font-regular mb-[20px] text-[12px]">{`${item.songs_count} пісень`}</Text>
        </View>
      </TouchableWithoutFeedback>
    );
  };

  return (
    <View>
      <View>
        <FlatList
          keyExtractor={(item) => 'playlist_' + item.id}
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

export default PlaylistCard