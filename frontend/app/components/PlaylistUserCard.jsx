import React, { useContext, useEffect, useState } from 'react';
import { View, Text, Image, TouchableWithoutFeedback, FlatList, TouchableOpacity, TextInput, Modal, Button } from 'react-native';
import { useRouter } from 'expo-router';
import dummyData from '../Mock/Dummy';
import { PlaylistContext } from '../../context/PlaylistContext';
import {createPlaylist} from '../../lib/handleFavourite';
import { getAccount, getUserID } from '../../lib/appwrite';
import {fetchPlaylistFullInfoFavourite} from '../../lib/handleFavourite';
import axios from 'axios';

const PlaylistUserCard = ({limit, fetchReccData}) => {

  if (limit==undefined) {
    limit = 0
  }
  console.log("limit", limit)
  const router = useRouter();
  const [favourite, setFavourite] = useState([]);

  const [playlist, setPlaylist] = useState([]);
  const fetchPlaylistData = async (limit) => {
    try {
      const result = await fetchPlaylistFullInfoFavourite(limit);
      // console.log("result ", result)
      setPlaylist(result);
    } catch (error) {
      console.error('Error fetching playlists:', error);
    }
  };
  useEffect(() => {
    fetchPlaylistData(limit);
    // fetchReccData();
  }, []);

  const createFavouritePlaylist = async () => {
    try {
      const userId = await getUserID();
      data = {
        'name' : newPlaylistName,
        'description' : null,
        'cover' : 0,
        'user_id' : userId,
        'for_user_id' : null
        }
      const response = await createPlaylist(data);
      setFavourite(response.data);
      fetchPlaylistData(limit);
      if (fetchReccData!=undefined) fetchReccData();
    } catch (error) {
      console.error('Error fetching favourite:', error);
    }
  };


  // console.log(favourite)

  const [modalVisible, setModalVisible] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState('');

  const { playlists, addPlaylist } = useContext(PlaylistContext);
  const [updatedPlaylists, setUpdatedPlaylists] = useState(playlists);

  const getSongCountText = (count) => {
    if (count === 0) {
      return '0 пісень';
    } else if (count === 1) {
      return `${count} пісня`;
    } else if (count >= 2 && count <= 4) {
      return `${count} пісні`;
    } else {
      return `${count} пісень`;
    }
  };

  const handleCreatePlaylist = () => {
    createFavouritePlaylist();
    setModalVisible(false);
    setNewPlaylistName('');
  };

  const _renderItem = ({ item, index }) => {
    const songCount = item.songs_count;
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
        <View style={{
          marginTop: 20,
          marginRight: index === item.songs_count - 1 ? 0 : 12,
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <View className="border border-blue/60 rounded-[8px]">
            <Image 
              key={index}
              source={item.background ? { uri: `https://i.scdn.co/image/${item.background}` } : require('../../assets/images/unknown_track.png')}
              className="w-[117px] h-[117px]"
            />
          </View>
          <Text className="w-full text-white font-regular text-[14px] mb-[4px] mt-[10px]">
            {item.name.length > 10 ? `${item.name.slice(0, 10)}...` : item.name}
          </Text>
          <Text className="w-full text-gray-100 font-regular text-[12px]">{getSongCountText(songCount)}</Text>
        </View>
      </TouchableWithoutFeedback> 
    );
  };

  return (
    <View>
      <View className="flex-row justify-between items-center">
        <Text className="text-white text-[20px] font-medium mt-[40px]">Ваші плейлисти</Text>
        <TouchableOpacity onPress={() => setModalVisible(true)}>
          <Text className="text-gray-200 text-[14px] font-medium mt-[40px]">(створити новий)</Text>
        </TouchableOpacity>
      </View>
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}
      >
        <View className="modal-container bg-black/60 w-full h-full flex justify-center absolute">
          <View className="modal-content bg-gray-200 rounded-[20px] px-4 py-4 flex justify-center">
            <TextInput
              className="text-dark font-regular text-[16px] mb-2 h-[40px] border-dark border py-[10px] pl-[10px] rounded-[8px]"
              onChangeText={text => setNewPlaylistName(text)}
              value={newPlaylistName}
              placeholder="Введіть назву нового плейлисту"
            />
            <FlatList 
              data={dummyData.DefaultThumbnails}
              keyExtractor={(item) => item.id}
              horizontal
              renderItem={({ item }) => (
                <TouchableOpacity>
                  <Image 
                    source={item.thumbnail}
                    className="w-[50px] h-[50px] rounded-[4px] mr-2"
                  />
                </TouchableOpacity>
              )}
            />
            <TouchableOpacity onPress={handleCreatePlaylist} className="bg-blue rounded-[8px] px-8 py-2 items-center">
              <Text className="text-[16px] font-regular text-white">Готово</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
      <View>
        <FlatList 
          data={playlist}
          keyExtractor={(item) => 'playlist_' + item.id}
          numColumns={3}
          renderItem={_renderItem}
        />
      </View>
    </View>
  );
  return null
};

export default PlaylistUserCard;
