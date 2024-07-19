import { TouchableOpacity, Image, Touchable, TouchableHighlight } from 'react-native';
import React from 'react';
import { useRouter } from 'expo-router';
import { icons } from '../../constants';
import FloatingPlayer from '../components/FloatingPlayer';

const PlayerButton = () => {
  const router = useRouter();

  const handlePlayerPress = () => {
    router.push('/player');
  };

  return (
    <TouchableHighlight onPress={handlePlayerPress}>
        <FloatingPlayer />
      {/* <Image source={icons.play} resizeMode="contain" /> */}
    </TouchableHighlight>
  );
};

export default PlayerButton;