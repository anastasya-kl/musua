import { View, Text, Image } from 'react-native'
import { Tabs, Redirect } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

import { icons } from '../../constants';
// import { useGlobalContext } from '../../context/GlobalProvider';
import { Colors } from 'react-native/Libraries/NewAppScreen';

const TabIcon = ({ icon, color, name, focused}) => {
    return (
        <View style={{
            alignItems: 'center', justifyContent: 'center', gap: 8
        }}>
            <Image 
                source={icon}
                resizeMode="contain"
                tintColor={color}
                style={{width: 24, height: 24}}
            />
        </View>
    )
}

const TabsLayout = () => {
    // const { user } = useGlobalContext();

  return (
    <>
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: '#A7C9FF',
                tabBarInactiveTintColor: '#7A7A7A',
                tabBarStyle: {
                    backgroundColor: '#04071B',
                    height: 64,
                    borderTopWidth: 0,
                }
            }}>
            <Tabs.Screen 
                name="home"
                options={{
                    title: 'Головна',
                    headerShown: false,
                    tabBarIcon: ({ color, focused }) => (
                        <TabIcon 
                            icon = {icons.home}
                            color = {color}
                            name = "Головна"
                            focused={focused}
                        />
                    )
                }}
            />
            <Tabs.Screen 
                name="search"
                options={{
                    title: 'Пошук',
                    headerShown: false,
                    tabBarIcon: ({ color, focused }) => (
                        <TabIcon 
                            icon = {icons.search}
                            color = {color}
                            name = "Пошук"
                            focused={focused}
                        />
                    )
                }}
            />
            <Tabs.Screen 
                name="library"
                options={{
                    title: 'Медіатека',
                    headerShown: false,
                    tabBarIcon: ({ color, focused }) => (
                        <TabIcon 
                            icon = {icons.library}
                            color = {color}
                            name = "Медіатека"
                            focused={focused}
                        />
                    )
                }}
            />
            <Tabs.Screen 
                name="profile"
                options={{
                    title: 'Обліковий запис',
                    headerShown: false,
                    tabBarIcon: ({ color, focused }) => (
                        <TabIcon 
                            icon = {icons.profile}
                            color = {color}
                            name = 'ViNa'
                            focused={focused}
                        />
                    )
                }}
            />
        </Tabs>
        <StatusBar backgroundColor='#04071B' style='light' />
    </>
  )
}

export default TabsLayout
