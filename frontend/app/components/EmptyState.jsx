import { View, Text, Image } from 'react-native'
import React from 'react'
import { images } from '../../constants'
import CustomButton from './CustomButton'
import { router } from 'expo-router'

const EmptyState = ({ title }) => {
  return (
    <View className="justify-center items-center px-4">
      <Image source={images.empty} 
      className="w-[212px] h-[170px]" resizeMode='contain' />
      
      <Text className="text-xl text-center font-regular text-white mt-2">
        {title}
      </Text>

      <CustomButton 
        title="Повернутися на головну"
        handlePress={() => router.push('/home')}
        containerStyles="w-full my-5"
      />
    </View>
  )
}

export default EmptyState