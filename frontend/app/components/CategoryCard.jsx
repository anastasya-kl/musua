import { View, Text, ImageBackground, TouchableOpacity, TouchableWithoutFeedback, FlatList, Image, TextInput, Modal, Button  } from 'react-native'
import React, {useState, useEffect} from 'react'
import { useRouter } from 'expo-router';
import dummyData from '../Mock/Dummy';
import axios from 'axios';


const CategoryCard = ({}) => {

  const router = useRouter();
  const [categories, setCategories] = useState([]);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://192.168.1.106:8080/api/get_all_categories_data/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const categoryImages = {
    1: require('../../assets/images/category-1.png'),
    2: require('../../assets/images/category-2.png'),
    3: require('../../assets/images/category-3.png'),
    4: require('../../assets/images/category-4.png'),
    5: require('../../assets/images/category-5.png'),
    6: require('../../assets/images/category-6.png'),
    7: require('../../assets/images/category-7.png'),
  };

    const _renderItem = ({ item, index }) => {
    const isOddItem = index % 2 !== 0;
    const isLastItem = index === categories.length - 1;

    const handlePress = () => {
      router.push({
        pathname: `/category/${item.id}`,
        params: { category: item },
      });
    };

    return (
      <View className="mb-4 mr-4 flex-1">
        <TouchableWithoutFeedback onPress={handlePress}>
          <ImageBackground
            source={categoryImages[item.id]}
            className="w-full h-[100px] rounded-[4px] overflow-hidden"
            resizeMode="cover"
          >
            <Text className="absolute w-[200px] text-[14px] font-regular text-white mt-[14px] ml-[14px]">
              {item.name}
            </Text>
          </ImageBackground>
        </TouchableWithoutFeedback>
      </View>
    )
  }

  return (
    <View className="mt-10">
    <FlatList
      data={categories}
      keyExtractor={(item) => `genre_${item.id}`}
      numColumns={2}
      renderItem={_renderItem}
    />
  </View>
  )
}

export default CategoryCard