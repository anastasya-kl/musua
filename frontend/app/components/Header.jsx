import { View, Text } from 'react-native'
import React from 'react'

const Header = ({ activeItem, item }) => {
  return (
    <View className="justify-between items-end flex-row mb-10">
              <View>
                <Text className="font-regular text-sm text-gray-100">
                  Ласкаво просимо
                </Text>
                <Text className="text-2xl font-regular text-white">
                  User
                </Text>
              </View>
              <View>
                <Pressable className="border rounded-[4px] border-blue px-[16px] py-[4px]">
                  <Text className="text-white font-regular text-[14px]">Музика</Text>
                </Pressable>
              </View>
              <View>
                <Pressable className="border rounded-[4px] border-blue px-[16px] py-[4px]">
                  <Text className="text-white font-regular text-[14px]">Підкасти</Text>
                </Pressable>
              </View>
              {/*<View className="w-[50px] h-[50px] mt-1.5">
                <Image 
                  source={images.profile}
                  className="w-full h-full rounded-[100px]"
                  resizeMode='cover'
                />
              </View>*/}
            </View>
  )
}

export default Header