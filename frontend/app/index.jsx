import { StatusBar } from 'expo-status-bar';
import 'react-native-url-polyfill/auto'
import { Text, View, Image, ScrollView } from 'react-native';
import { Redirect, router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { images } from '../constants';
import CustomButton from './components/CustomButton';
import { useGlobalContext } from '../context/GlobalProvider';


export default function App() {
  const { isLoading, isLoggedIn } = useGlobalContext();

  if(!isLoading && isLoggedIn) return <Redirect href="/home"/>

  return (
    <SafeAreaView style={{backgroundColor: '#04071B', height: '100%'}}>
      <ScrollView contentContainerStyle={{height: 'full'}}>
        <View style={{
          justifyContent: 'center', alignItems: 'center',
          width: 'full', marginTop: 60
        }}>
          <Image 
            source={require('../assets/images/logo.png')}
            style={{width: 146, height: 40}}
            resizeMode='contain'
          />
          
          <View style={{position: 'relative'}}>
            <Text style={{fontFamily: 'NAMU1750', fontSize: 34,
            textAlign: 'center', color: '#ffffff', marginTop: 160}}>Вітаємо в MUSUA!</Text>
            <Text style={{fontFamily: 'NAMU1750', fontSize: 18,
            textAlign: 'center', color: '#9D9D9D', marginTop: 20}}>Пориньте у світ української музики</Text>

            <CustomButton 
              title="Розпочнімо"
              handlePress = {() => router.push('/sign-in')}
              containerStyles="w-[324px] mt-7"
            />
          </View>

        </View>
      </ScrollView>
      
      <StatusBar backgroundColor='#04071B'
      style='light' />
    </SafeAreaView>
  );
}
