/**
 * NAV-LOSEN MVP - MAIN APP
 * Created: 20. oktober 2025
 * Author: Manus (Agent #6)
 * Description: Main entry point for NAV-Losen mobile app
 */

import React, { useEffect, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator } from 'react-native';

// Supabase
import { supabase, getSession } from './src/services/supabase';

// Screens (to be created)
import WelcomeScreen from './src/screens/WelcomeScreen';
import QuadrantScreen from './src/screens/QuadrantScreen';
import EmotionWheelScreen from './src/screens/EmotionWheelScreen';
import DefinitionScreen from './src/screens/DefinitionScreen';
import PressureSignalsScreen from './src/screens/PressureSignalsScreen';
import LiraChatScreen from './src/screens/LiraChatScreen';
import RecommendationsScreen from './src/screens/RecommendationsScreen';
import AuthScreen from './src/screens/AuthScreen';

const Stack = createStackNavigator();

export default function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [session, setSession] = useState(null);

  useEffect(() => {
    // Check for existing session
    getSession().then((session) => {
      setSession(session);
      setIsLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000' }}>
        <ActivityIndicator size="large" color="#fff" />
      </View>
    );
  }

  return (
    <>
      <StatusBar style="light" />
      <NavigationContainer>
        <Stack.Navigator
          screenOptions={{
            headerStyle: { backgroundColor: '#000' },
            headerTintColor: '#fff',
            headerTitleStyle: { fontWeight: 'bold' },
            cardStyle: { backgroundColor: '#000' },
          }}
        >
          {!session ? (
            // Auth flow
            <Stack.Screen
              name="Auth"
              component={AuthScreen}
              options={{ headerShown: false }}
            />
          ) : (
            // Main app flow (Mestringsside 6 phases)
            <>
              <Stack.Screen
                name="Welcome"
                component={WelcomeScreen}
                options={{ title: 'Velkommen til NAV-Losen' }}
              />
              <Stack.Screen
                name="Quadrant"
                component={QuadrantScreen}
                options={{ title: 'Hvordan føler du deg?' }}
              />
              <Stack.Screen
                name="EmotionWheel"
                component={EmotionWheelScreen}
                options={{ title: 'Velg følelse' }}
              />
              <Stack.Screen
                name="Definition"
                component={DefinitionScreen}
                options={{ title: 'Hva betyr dette?' }}
              />
              <Stack.Screen
                name="PressureSignals"
                component={PressureSignalsScreen}
                options={{ title: 'Trykk og signaler' }}
              />
              <Stack.Screen
                name="LiraChat"
                component={LiraChatScreen}
                options={{ title: 'Chat med Lira' }}
              />
              <Stack.Screen
                name="Recommendations"
                component={RecommendationsScreen}
                options={{ title: 'Anbefalinger' }}
              />
            </>
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
}

