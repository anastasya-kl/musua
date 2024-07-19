import { View, Text, Image, Pressable } from 'react-native'
import React from 'react'
import { icons } from '../../constants';
import { Link, useRouter } from 'expo-router';

import { LinearGradient } from 'expo-linear-gradient';


const FloatingPlayer = ({ title, artist, thumbnail }) => {

    const router = useRouter();

    const handlePress = () => {
        console.log("Navigating to player screen");
        router.push({
            pathname: '/player',
            params: { 
                title: title, 
                artist: artist, 
                thumbnail: thumbnail 
            }
        });
    };

    return (
            <Pressable onPress={handlePress}>
                <LinearGradient
                    colors={['#211932', '#04071B']}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 0, y: 1 }}
                    style={{
                        width: '100%',
                        height: 84,
                        borderTopLeftRadius: 20,
                        borderTopRightRadius: 20,
                        paddingHorizontal: 16,
                        paddingVertical: 12,
                    }}>
                    <View className="flex-row justify-between items-center" >
                        <View className="flex-row items-center">
                            <Image 
                                source={ {uri: 'https://i.scdn.co/image/ab67616d00001e0274f063b66b6a0812cae4fb2a'} }
                                className="w-[60px] h-[60px] rounded-[60px]"
                            />
                            <View className="ml-[16px]">
                                <Text className="font-medium text-white text-[14px]">Popelushka</Text>
                                <Text className="font-medium text-gray-100 w-[135px] text-[12px] mt-[2px]">Qarpa</Text>
                            </View>
                        </View>

                        <View className="flex-row items-center">
                            <Image source={icons.playBack} className="w-[26px] h-[26px] mr-[5px]" />
                            <Image source={icons.play} className="w-[40px] h-[40px] mr-[5px]" />
                            <Image source={icons.playGo} className="w-[26px] h-[26px]" />
                        </View>    
                    </View>
                </LinearGradient>
            </Pressable>
        
    )
}

export default FloatingPlayer;