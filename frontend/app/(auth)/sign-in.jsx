import { View, Text, ScrollView, Image, Dimensions, Alert } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import images from '../../constants/images'
import FormField from '../components/FormField'
import CustomButton from '../components/CustomButton'
import { Link, router } from 'expo-router'
import { signIn } from '../../lib/appwrite'

const SignIn = () => {
  const [form, setForm] = useState({
    email: '',
    password: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const submit = async () => {
    if(!form.email || !form.password){
      Alert.alert('Error', 'Будь ласка заповніть всі поля')
    }
    
    setIsSubmitting(true);

    try {
      await signIn(form.email, form.password)

      // set it to global state...

      router.replace('/home')
    } catch (error) {
      Alert.alert('Error', error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <SafeAreaView className="bg-backg h-full">
      <ScrollView>
        <View className="w-full justify-center min-h-[80vh] px-4 my-6"
        style={{
          minHeight: Dimensions.get("window").height - 100,
        }}>
          <Image 
            source={images.logo}
            resizeMode='contain'
            className="w-[120px] h-[32px] mb-4"
          />

          <FormField 
            title = "Email"
            value = {form.email}
            handleChangeText={(e) => setForm({ ...form,
            email: e })}
            otherStyles = "mt-7"
            keyboardType = "email-address"
          />
          <FormField 
            title = "Пароль"
            value = {form.password}
            handleChangeText={(e) => setForm({ ...form,
            password: e })}
            otherStyles = "mt-7"
          />

          <CustomButton 
            title = "Увійти"
            handlePress={submit}
            containerStyles="mt-7"
            isLoading={isSubmitting}
          />

          <View className="justify-center pt-5 flex-row gap-2">
              <Text className="text-[16px] text-gray-100 font-regular">
              Не має акаунту?
              </Text>
              <Link href="/sign-up" className='text-[16px] font-medium text-blue'>Зареєструватися</Link>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  )
}

export default SignIn