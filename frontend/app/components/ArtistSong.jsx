import { View, Text, Image, FlatList, Pressable } from 'react-native';
import React, {useState, useEffect} from 'react';
import dummyData from '../Mock/Dummy';
import { icons } from '../../constants';
import axios from 'axios';

const ArtistSong = ({ artistId }) => {
  const [songsData, setSongsData] = useState(null);
  const fetchSongsData = async (artistId) => {
    try {
      const response = await axios.get(`http://192.168.1.106:8080/api/songs_full_info_by_artist/${artistId}`);
      setSongsData(response.data);
    } catch (error) {
      console.error('Error fetching songs data:', error);
    }
  };
  
  useEffect(() => {
    if (artistId) {
      fetchSongsData(artistId);
    }
  }, [artistId]);

  const _renderItem = ({ item, index }) => {

    const artists = item.artists.map((artist) => artist.name).join(', ');

    return (
      <View className="flex-row items-start justify-between mt-[6px] mb-[16px]">
        <View className="flex-row items-center">
          <View>
            <Image
              key={index}
              source={{ uri: `https://i.scdn.co/image/${item.album.background}` }}
              className="w-[60px] h-[60px] rounded-[42px]"
            />
          </View>
          <View className="ml-[12px]">
            <Text className="font-medium text-white text-[14px]">{item.song.name}</Text>
            <Text className="font-medium text-gray-100 text-[12px] mt-[2px]">{artists}</Text>
          </View>
        </View>
        <View className="mr-[10px] mt-[18px]"><Image source={icons.like} /></View>
        
      </View>
    );
  };

  return (
    <Pressable>
      <View className="mb-[20px]">
        <View>
          <FlatList
            keyExtractor={(item) => item.song.id.toString()}
            contentContainerStyle={{}}
            data={songsData}
            renderItem={_renderItem}
          />
        </View>
      </View>
    </Pressable>
  );
  return null
};

export default ArtistSong;
