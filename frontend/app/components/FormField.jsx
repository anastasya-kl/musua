import { View, Text, TextInput, TouchableOpacity, Image } from 'react-native'
import React, { useState } from 'react'

import { icons } from '../../constants'

const FormField = ({ title, value, placeholder,
handleChangeText, otherStyles, ...props }) => {
  const [showPassword, setShowPassword] = useState(false)
  
  return (
    <View className={`space-y-2 ${otherStyles}`}>
      <Text className="text-[16px] text-gray-200 font-regular">{title}</Text>

      <View className="border-2 border-black-200 w-full h-16 px-4 bg-black-100 rounded-[8px]
      focus:border-blue items-center flex-row">
        <TextInput 
          className="flex-1 text-white font-regular text-base"
          value={value}
          placeholder={placeholder}
          placeholderTextColor="#7b7b8b"
          onChangeText={handleChangeText}
          secureTextEntry={title === 'Пароль' && !showPassword}
        />

        {title === 'Пароль' && (
          <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
            <Image source={!showPassword ? icons.eye :
            icons.eyeHide } className="w-6 h-6"
            resizeMode='contain' />
          </TouchableOpacity>
        )}
      </View>
    </View>
  )
}

export default FormField