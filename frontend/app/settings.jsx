import { View, Text, TouchableOpacity, Image } from 'react-native'
import React from 'react'
import { icons } from '../constants'
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const SettingScreen = () => {
    const router = useRouter();

    const handleBackPress = () => {
        router.back();
    };

  return (
    <SafeAreaView>
        <View className="bg-backg h-full">
            <View className="px-4 flex-row justify-between items-start mt-4">
                <TouchableOpacity onPress={handleBackPress}>
                    <Image 
                        source={icons.arrowDown}
                        className="w-[36px] h-[36px] mt-[4px]"
                    />
                </TouchableOpacity>
                <Text className="text-white font-medium text-[28px] mb-4">Налаштування</Text>
            </View>
            <View 
                className="bg-white/30 h-[1px] w-full"
            />
        </View>
    </SafeAreaView>
  )
}

export default SettingScreen

