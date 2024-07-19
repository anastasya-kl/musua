import { View, Text, FlatList, Image, RefreshControl, Alert, Pressable, ScrollView } from 'react-native'
import React, { useEffect, useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context';

import { images } from '../../constants'
import SearchInput from '../components/SearchInput'
import Trending from '../components/Trending'
import EmptyState from '../components/EmptyState'
import SongCard from '../components/SongCard'
import { getAllPosts, getLatestPosts } from '../../lib/appwrite'
import useAppwrite from '../../lib/useAppwrite'
import FloatingPlayer from '../components/FloatingPlayer'
import PlaylistCard from '../components/PlaylistCard'
import ArtistCard from '../components/ArtistCard'
import PlaylistUserCard from '../components/PlaylistUserCard'

import { useNavigation } from '@react-navigation/native';
import PlayerButton from '../components/PlayerButton';
import { useGlobalContext } from '../../context/GlobalProvider';
import {fetchPlaylistFullInfoFavourite} from '../../lib/handleFavourite';
import {fetchRecommendations} from '../../lib/handleReccomendations';

import { getAccount, getUserID } from '../../lib/appwrite';
import axios from 'axios';
import {shuffleDataRandom, shuffleData} from '../../lib/manageData';
import { FetchFunctionsContext } from '../../context/FetchFunctionsContext';

const Home = ({}) => {
  const { user } = useGlobalContext();
  const [refreshing, setRefreshing] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  
  // const [favourite, setFavourite] = useState([]);

  // const fetchPlaylistData = async (limit) => {
  //   try {
  //     const result = await fetchPlaylistFullInfoFavourite(limit);
  //     // console.log("result ", result)
  //     setFavourite(result);
  //   } catch (error) {
  //     console.error('Error fetching playlists:', error);
  //   }
  // };

  const fetchReccData = async () => {
    try {
      const result = await fetchRecommendations();
      // console.log("result ", result)
      setRecommendations(result);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  useEffect(() => {
    // fetchPlaylistData(3);
    fetchReccData();
  }, []);
  
  const updateRecommendations = async () => {
    try {
      const result = shuffleData(recommendations);
      
      setRecommendations(result);
    } catch (error) {
      console.error('Error updating recommendations:', error);
    }
  };
  const onRefresh = async () => {
    setRefreshing(true);
    await updateRecommendations();
    // await refetch();
    // await fetchReccData();
    setRefreshing(false);
  };

  return (
    <SafeAreaView className="bg-backg h-full">
      <FlatList 
        ListHeaderComponent={() => (
          <View className="my-6 px-4 space-y-6">
            <View className="justify-between items-center flex-row mb-10">
              <View className="w-[50px] h-[50px] border border-blue rounded-[100px] items-center justify-center">
                <Image 
                  source={{ uri: user?.avatar }}
                  className="w-[90%] h-[90%] rounded-[100px]"
                  resizeMode='cover'
                />
              </View>
              <View>
                <Text className="text-white font-regular text-[14px]">Ласкаво просимо</Text>
                <Text className="text-white font-regular text-[20px] text-right mt-[8px]">{ user?.username }</Text>  
               </View>
            </View>


            <SearchInput />
            <View key={'user'} className="mb-[20px]">
                    <PlaylistUserCard limit={3} fetchReccData={fetchReccData}/>
            </View>
            {recommendations.map((recommendation) => {
              if (recommendation.type === 'Song') {
                return (
                  <View key={recommendation.title} className="mb-[20px]">
                    <Text className="text-white text-[20px] font-medium mb-[20px]">{recommendation.title}</Text>
                    <SongCard data={recommendation.data} />
                  </View>
                );
              } else if (recommendation.type === 'Artist') {
                return (
                  <View key={recommendation.title} className="mb-[20px]">
                    <Text className="text-white text-[20px] font-medium mb-[20px]">{recommendation.title}</Text>
                    <ArtistCard data={recommendation.data} />
                  </View>
                );
              } else if (recommendation.type === 'Playlist') {
                return (
                  <View key={recommendation.title} className="mb-[20px]">
                    <Text className="text-white text-[20px] font-medium mb-[20px]">{recommendation.title}</Text>
                    <PlaylistCard data={recommendation.data} />
                  </View>
                );
              }
              return null;
            })}
          </View>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      />

      <FloatingPlayer />
    </SafeAreaView>
  );
};

export default Home;

// const Home = ({}) => {

//   const navigation = useNavigation();

//   const { data: posts, refetch } = useAppwrite(getAllPosts);
//   const { data: latestPosts } = useAppwrite(getLatestPosts);

//   const [refreshing, setRefreshing] = useState(false)

//   const [recommendations, setRecommendations] = useState([]);

//   const fetchRecommendations = async (userId) => {
//     try {
//       const response = await axios.get(`http://192.168.1.106:8080/api/create_complex_reccomendations/${userId}`);
//       setRecommendations(response.data);
//     } catch (error) {
//       console.error('Error fetching recommendations:', error);
//     }
//   };
  
//   useEffect(() => {
//     const fetchUserId = async () => {
//       try {
//         const userId = await getUserID();
//         // console.log("userId", userId);
//         fetchRecommendations(userId);
//       } catch (error) {
//         console.error('Error fetching userId:', error);
//       }
//     };
  
//     fetchUserId();
//   }, []);
//   // console.log(recommendations);

//   const onRefresh = async () => {
//     setRefreshing(true);
//     await refetch();
//     const userId = await getUserID();
//     fetchRecommendations(userId);
//     setRefreshing(false);
//   }

//   return (
//     <SafeAreaView className="bg-backg h-full">
//       <FlatList 
//         ListHeaderComponent={() => (
//           <View className="my-6 px-4 space-y-6">

//             <View className="justify-between items-center flex-row mb-10">
//               <View className="w-[50px] h-[50px]">
//                 <Image 
//                   source={images.profile}
//                   className="w-full h-full rounded-[100px]"
//                   resizeMode='cover'
//                 />
//               </View>
//               <View>
//                 <Text className="text-white font-regular text-[14px]">Ласкаво просимо</Text>
//                 <Text className="text-white font-regular text-[20px] text-right mt-[8px]">User</Text>  
//                </View>
//             </View>

//             <SearchInput />


//             <View className="w-full flex-1 pt-5">

//               <View className="mb-[20px]">
//                 <Text className="text-white text-[20px] font-medium mb-[20px]">
//                   Рекомендації для вас
//                 </Text>
//                 <SongCard />
//               </View>

//               <ArtistCard/>

//               <View className="mt-[40px]">
//                 <Text className="text-white text-[20px] font-medium mb-[20px]">
//                   Популярні
//                 </Text>
//                 <Trending posts={latestPosts ?? []} />
//               </View>

//               <PlaylistCard></PlaylistCard>
//             </View>
//           </View>
//         )}
//         refreshControl={<RefreshControl 
//           refreshing={refreshing} onRefresh={onRefresh}
//         />}
//       />

//       <FloatingPlayer />
//     </SafeAreaView>
//   )
// }
