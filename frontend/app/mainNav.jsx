// app/MainNavigation.jsx
import { View, Text, TouchableOpacity } from 'react-native';
import React from 'react';
import { useNavigation } from '@react-navigation/native';

const MainNavigation = ({ children }) => {
  const navigation = useNavigation();

  const navigateToHome = () => {
    navigation.navigate('Home');
  };

  const navigateToCategories = () => {
    navigation.navigate('Categories');
  };

  return (
    <View style={{ flex: 1 }}>
      {children}
      <View style={{ flexDirection: 'row', justifyContent: 'space-around', paddingVertical: 10, backgroundColor: 'lightgrey' }}>
        <TouchableOpacity onPress={navigateToHome}>
          <Text>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={navigateToCategories}>
          <Text>Categories</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default MainNavigation;
