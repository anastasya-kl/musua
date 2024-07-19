// import TrackPlayer from 'react-native-track-player'

// module.exports = async function () {
//     TrackPlayer.addEventListener('remote-play', () =>
//     TrackPlayer.play());

//     TrackPlayer.addEventListener('remote-pause', () =>
//     TrackPlayer.pause());
// }

// player.jsx

import { View, Text, SafeAreaView, Image, TouchableOpacity, Animated } from 'react-native'
import 'nativewind';
import { icons, images } from '../constants';
import dummyData from './Mock/Dummy';
import { useRouter } from 'expo-router';

const PlayerScreen = () => {
  const router = useRouter();
  const { params } = router;

  if (!params) {
    return <Text>No song data available</Text>;
  }

  const { title, artist, thumbnail } = params;

  const handleBackPress = () => {
    router.back();
  };

  return (
    <SafeAreaView className="bg-dark h-full">
      <View className="flex-1 px-4 mt-8">
        <View className="flex-row mt-6 justify-between items-center">
          <TouchableOpacity onPress={handleBackPress}>
            <Image 
              source={icons.arrowDown}
              className="w-[42px] h-[42px]"
            />
          </TouchableOpacity>
          <Image 
            source={icons.playlistList}
            className="w-[42px] h-[42px]"
          />
        </View>

        <View className="items-center my-[50px]">
          <Image 
            source={thumbnail}
            className="w-[250px] h-[250px] rounded-[8px]"
          />
        </View>

        <View className="flex-row justify-between items-center">
          <Image 
            source={icons.like}
            className="w-[30px] h-[30px]"
          />
          <View className="items-center">
            <Text className="text-white font-NAMU1750 text-[32px] mb-[12px]">{title}</Text>
            <Text className="text-white font-NAMU1750 text-[16px]">{artist}</Text>
          </View>
          <Image 
            source={icons.menu}
            className="w-[30px] h-[30px]"
          />
        </View>

        <View className="mt-[64px]">
          <View className="flex-row justify-between">
            <Text className="text-white font-NAMU1990">0:00</Text>
            <Text className="text-white font-NAMU1990">4:13</Text>
          </View>
          <View className="h-[2px] bg-gray-100 mt-[10px]"></View>
        </View>

        <View className="flex-row justify-between items-center px-[30px] mt-10">
          <Image 
            source={icons.shuffle}
            className="w-[25px] h-[25px]"
          />
          <View className="flex-row items-center">
            <Image source={icons.playBack} className="w-[35px] h-[35px] mr-[12px]" />
            <Image source={icons.play} className="w-[62px] h-[62px] mr-[12px]" />
            <Image source={icons.playGo} className="w-[35px] h-[35px]" />
          </View>
          <Image 
            source={icons.repeat}
            className="w-[25px] h-[25px]"
          />
        </View>
      </View>
    </SafeAreaView>
  );
};

export default PlayerScreen;
