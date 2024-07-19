import { View, Text, TouchableOpacity, Image } from 'react-native'
import React from 'react'
import { icons } from '../constants'
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const SupportScreen = () => {
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
                <Text className="text-white font-medium text-[28px] mb-4">Підтримка</Text>
            </View>
            <View 
                className="bg-white/30 h-[1px] w-full"
            />
            <View className="mt-6 px-4">
                <View className="flex-row items-start">
                    <Text className="text-white font-medium text-[20px] mr-[16px]">Тел.:</Text>
                    <View className="pt-[6px]">
                        <Text className="text-blue font-regular text-[16px] mb-[12px]">+38098-765-43-21  
                        <Text className="text-gray-200 font-regular text-[16px]"> (Вікторія)</Text></Text>

                        <Text className="text-blue font-regular text-[16px] mb-[8px]">+38097-890-12-34  
                        <Text className="text-gray-200 font-regular text-[16px]"> (Анастасія)</Text></Text>
                    </View>
                </View>

                <View className="flex-row items-start mt-8">
                    <Text className="text-white font-medium text-[20px] mr-[16px]">Пошта:</Text>
                    <Text className="text-blue font-regular text-[16px] mb-[12px]">musua@gmail.com</Text>
                </View>
            </View>
        </View>
    </SafeAreaView>
  )
}

export default SupportScreen