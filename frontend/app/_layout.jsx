import { Text, View } from 'react-native'
import { SplashScreen, Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import { useEffect } from 'react';
import 'nativewind';

import GlobalProvider from '../context/GlobalProvider';
import { PlaylistProvider } from '../context/PlaylistContext';
// import { PlayerProvider } from '../context/';

SplashScreen.preventAutoHideAsync();

const RootLayout = () => {

    const [fontsLoaded, error] = useFonts({
        "NAMU1990": require("../assets/fonts/NAMU1990.otf"),
        "NAMU1750": require("../assets/fonts/NAMU1750.otf")
    });

    useEffect(() => {
        if(error) throw error;

        if(fontsLoaded) SplashScreen.hideAsync();
        }, [fontsLoaded, error])

        if(!fontsLoaded && !error) return null;

    return (
        <GlobalProvider> 
            <PlaylistProvider>
                <Stack>
                    <Stack.Screen name='index' options={{ headerShown: false}} />
                    <Stack.Screen name='(auth)' options={{ headerShown: false}} />
                    <Stack.Screen name='(tabs)' options={{ headerShown: false}} />
                    <Stack.Screen name='search/[query]' options={{ headerShown: false}} />
                    {/* <Stack.Screen name='player' options={{ headerShown: false}} /> */}
                    <Stack.Screen name='player/[playerId]' options={{ headerShown: false}} />
                    <Stack.Screen name='artist/[artistId]' options={{ headerShown: false}} />
                    <Stack.Screen name='playlist/[playlistId]' options={{ headerShown: false}} />
                    <Stack.Screen name='category/[categoryId]' options={{ headerShown: false}} />
                    <Stack.Screen name='favorite/[favoriteId]' options={{ headerShown: false}} />
                    <Stack.Screen name='settings' options={{ headerShown: false }} />
                    <Stack.Screen name='support' options={{ headerShown: false }} />
                </Stack>
                {/* <FloatingPlayer /> */}
            </PlaylistProvider>
        </GlobalProvider>
    )
}

export default RootLayout