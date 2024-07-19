import { View, Text, FlatList, Image, RefreshControl, Alert, Pressable, TouchableOpacity } from 'react-native'
import React, { useEffect, useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import * as ImagePicker from 'expo-image-picker';

import { images } from '../../constants'
import { getAllPosts, getLatestPosts, signOut } from '../../lib/appwrite'
import useAppwrite from '../../lib/useAppwrite'
import { useGlobalContext } from '../../context/GlobalProvider'
import { router, useRouter } from 'expo-router'

const Profile = ({}) => {
  const router = useRouter();

  const handleSettingsPress = () => {
    router.push('/settings');
  };

  const handleSupportPress = () => {
    router.push('/support');
  };

  const { user, setUser, setIsLoggedIn } = useGlobalContext();
  const [refreshing, setRefreshing] = useState(false)
  const { data: refetch } = useAppwrite(getAllPosts);

  const [profileImage, setProfileImage] = useState({ uri: user?.avatar}); 

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch(); 
    setRefreshing(false);
  }

  const logout = async () => {
    await signOut();
    setUser(null)
    setIsLoggedIn(false)

    router.replace('/sign-in')
  }

  const changeProfileImage = async () => {
    // Запит дозволу на доступ до галереї
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Вибачте, нам потрібен дозвіл для доступу до ваших фотографій!');
      return;
    }
  
    // Вибір зображення з галереї
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 4],
      quality: 1,
    });

    console.log('ImagePicker result:', result);
  
    if (!result.canceled) {
      setProfileImage({ uri: result.uri });
    }
  };
  
  return (
    <SafeAreaView className="bg-backg h-full">
      <View style={{ flex: 1, justifyContent: 'space-between' }}>
        <FlatList 
          ListHeaderComponent={() => (
            <View className="my-6 px-4 space-y-6">
              <View className="justify-center items-center">
                <View className="w-[100px] h-[100px] border border-blue rounded-[100px] items-center justify-center">
                  <Image 
                    source={profileImage} 
                    // className="w-[90%] h-[90%] rounded-[100px]"
                    style={{ width: '90%', height: '90%', borderRadius: 100 }}
                    resizeMode='cover'
                  />
                </View>
                <Text className="text-white font-regular text-[24px] mt-4">{ user?.username }</Text>
                <TouchableOpacity onPress={changeProfileImage}>
                  <Text className="text-gray-100 font-regular text-[16px] mt-[14px]">Змінити фото</Text>
                </TouchableOpacity>
              </View>

              <View className="h-[1px] bg-white/20 mt-[20px]"></View>

              <View className="pt-5 space-y-4 mb-8">
                <TouchableOpacity onPress={handleSettingsPress}>
                  <Text className="text-white text-[20px] font-medium mb-[20px]">Налаштування</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={handleSupportPress}>
                  <Text className="text-white text-[20px] font-medium mb-[20px]">Підтримка</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
          refreshControl={<RefreshControl 
            refreshing={refreshing} onRefresh={onRefresh}
          />}
        />
      </View>
      <View className="mb-[40px]">
        <TouchableOpacity onPress={logout} className="border rounded-[8px] border-purple px-[48px] py-[20px] justify-center items-center">
          <Text className="text-purple text-[16px] font-regular text-center">Вийти з облікового запису</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  )
}

export default Profile