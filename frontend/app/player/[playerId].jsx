import React, { useEffect, useState } from 'react';
import { View, Text, SafeAreaView, Image, TouchableOpacity } from 'react-native';
import Slider from '@react-native-community/slider';
import { Audio } from 'expo-av';
import { icons, images } from '../../constants';
import { useRouter, useLocalSearchParams } from 'expo-router';
import dummyData from '../Mock/Dummy';
import {fetchSongInfo} from '../../lib/getSongs';
import {getFavouriteSongIds} from '../../lib/handleQueue';

const PlayerScreen = () => {
  // console.log("here");
  const { playerId, dataContextData } = useLocalSearchParams();
  // console.log("datatId", playerId);
  // console.log(dataContextData);
  songIndex = playerId;
  const [currentSongIndex, setCurrentSongIndex] = useState(songIndex);
  const [sound, setSound] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackStatus, setPlaybackStatus] = useState(null);
  const router = useRouter();
  const [currentSongData, setCurrentSongData] = useState(null);

  const [song, setSong] = useState();
  useEffect(() => {
    const loadSound = async () => {
      console.log("currentSongIndex ", currentSongIndex)
      const currentSong = await fetchSongInfo(currentSongIndex);
      console.log("currentSong ", currentSong)
      if (currentSong.song.id && currentSong.song.preview_url_id) {
        setCurrentSongData(currentSong);
        const URL = "https://p.scdn.co/mp3-preview/" + currentSong.song.preview_url_id;

        // console.log("song", URL)
        const { sound } = await Audio.Sound.createAsync({ uri: `${URL}`});
        sound.setOnPlaybackStatusUpdate(updatePlaybackStatus);
        setSound(sound);
        await sound.playAsync();
        setIsPlaying(true);
      }
    };

    loadSound();

    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, [currentSongIndex]);


  useEffect(() => {
    const interval = setInterval(() => {
      if (sound && isPlaying) {
        sound.getStatusAsync().then(updatePlaybackStatus);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [sound, isPlaying]);

  const updatePlaybackStatus = status => {
    setPlaybackStatus(status);
  };

  const handlePlayPause = async () => {
    if (sound) {
      if (isPlaying) {
        await sound.pauseAsync();
        setIsPlaying(false);
      } else {
        await sound.playAsync();
        setIsPlaying(true);
      }
    }
  };

  const handleBackPress = () => {
    if (sound) {
      sound.stopAsync();
    }
    router.back();
  };

  const getFormattedTime = (milliseconds) => {
    const minutes = Math.floor(milliseconds / 60000);
    const seconds = Math.floor((milliseconds % 60000) / 1000);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  const handleSliderValueChange = async (value) => {
    if (sound && playbackStatus) {
      const newPosition = value * playbackStatus.durationMillis;
      await sound.setPositionAsync(newPosition);
    }
  };

  const [dataQueue, setDataQueue] = useState([]);
  useEffect(() => {
    const fetchFavoriteSongIds = async () => {
      try {
        const favoriteSongIds = await getFavouriteSongIds();
        setDataQueue(favoriteSongIds);
      } catch (error) {
        console.error('Error fetching favorite song IDs:', error);
      }
    };
  
    fetchFavoriteSongIds();
  }, []);

// -----------
  const handleNextSong = () => {
    if (!dataQueue || dataQueue.length === 0) {
      // Немає пісень в черзі, нічого не робимо
      return;
    }

    const currentIndex = dataQueue.indexOf(currentSongIndex);
    const nextIndex = currentIndex === dataQueue.length - 1 ? 0 : currentIndex + 1;
    console.log("currentSongIndex: ", currentSongIndex);
    console.log("nextIndex: ", dataQueue[nextIndex]);
    setCurrentSongIndex(dataQueue[nextIndex]);

    if (sound) {
      sound.stopAsync();
      // Можливо, тут потрібно завантажити та відтворити наступну пісню з dataQueue[nextIndex]
    }
  };

  const handlePreviousSong = () => {
    if (!dataQueue || dataQueue.length === 0) {
        return;
    }

    const currentIndex = dataQueue.indexOf(currentSongIndex);
    const previousIndex = currentIndex === 0 ? dataQueue.length - 1 : currentIndex - 1;
    console.log("currentSongIndex: ", currentSongIndex);
    console.log("previousIndex: ", dataQueue[previousIndex]);
    setCurrentSongIndex(dataQueue[previousIndex]);

    if (sound) {
        sound.stopAsync();
        // Можливо, тут потрібно завантажити та відтворити попередню пісню з dataQueue[previousIndex]
    }
  };


  // console.log("currentSongData", currentSongData)
  if (!currentSongIndex || !currentSongData) {
    return <Text>No song data available</Text>;
  }
  
  const artists = currentSongData.artists.map((artist) => artist.name).join(', ');
  // console.log("artist", artists)sound.stopAsync();
  // console.log(`https://i.scdn.co/image/${currentSongData.album.background}`)
  return (
    <SafeAreaView className="bg-dark h-full">
      <View className="flex-1 px-4 mt-8">
        <View className="flex-row mt-6 justify-between items-center">
        <TouchableOpacity onPress={() => {
              sound.stopAsync();
              handleBackPress();
            }}>
            <Image 
              source={icons.arrowDown}
              className="w-[42px] h-[42px]"
            />
          </TouchableOpacity>
          <TouchableOpacity>
            <Image 
              source={icons.menu}
              className="w-[32px] h-[32px]"
            />
          </TouchableOpacity>
        </View>

        <View className="items-center my-[50px]">
          <Image 
            source={{ uri: `https://i.scdn.co/image/${currentSongData.album.background}` }}
            className="w-[250px] h-[250px] rounded-[8px]"
          />
        </View>

        <View className="justify-center items-center">
          <Text numberOfLines={1} ellipsizeMode="tail" className="text-white w-[300px] text-center font-NAMU1750 text-[30px] mb-[12px]">{currentSongData.name}</Text>
          <Text numberOfLines={1} ellipsizeMode="tail" className="text-white w-[290px] text-center font-NAMU1750 text-[16px]">{artists}</Text>
        </View>

        <View className="mt-[40px]">
          <View className="flex-row justify-between">
            <Text className="text-white font-NAMU1990">
              {playbackStatus ? getFormattedTime(playbackStatus.positionMillis) : '0:00'}
            </Text>
            <Text className="text-white font-NAMU1990">
              {playbackStatus ? getFormattedTime(29000) : '0:00'}
              </Text>
          </View>
          <Slider
            style={{ width: '100%', height: 40 }}
            minimumValue={0}
            maximumValue={1}
            value={playbackStatus ? playbackStatus.positionMillis / 29000 : 0}
            minimumTrackTintColor="#6496E7"
            maximumTrackTintColor="#FFFFFF"
            thumbImage={require('../../assets/icons/Rectangle.png')}
            onSlidingComplete={handleSliderValueChange}
          />
        </View>

        <View className="flex-row justify-center items-center mt-5">
          <View className="flex-row justify-center items-center">
            <TouchableOpacity onPress={handlePreviousSong}>
              <Image 
                source={icons.playBack}
                className="w-[35px] h-[35px] mr-[20px]"
              />
            </TouchableOpacity>
            <View className="flex-row items-center">
              <TouchableOpacity onPress={handlePlayPause}>
                <Image 
                  source={isPlaying ? icons.pause : icons.play}
                  className="w-[62px] h-[62px] mr-[20px]"
                />
              </TouchableOpacity>
            </View>
            <TouchableOpacity onPress={handleNextSong}>
              <Image 
                source={icons.playGo}
                className="w-[35px] h-[35px]"
              />
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
};

export default PlayerScreen;
