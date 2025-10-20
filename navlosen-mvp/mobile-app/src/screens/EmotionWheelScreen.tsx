/**
 * NAV-LOSEN MVP - EMOTION WHEEL SCREEN (Mestringsside Fase 3)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #6)
 * Description: Scrollable emotion wheel with 100 unique shapes (to be implemented by Nyra)
 * TODO: Implement 100 unique SVG shapes per quadrant
 */

import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

// Placeholder emotion data (will be replaced with full 100 emotions + SVG shapes)
const EMOTIONS = {
  red: ['Enraged', 'Panicked', 'Stressed', 'Furious', 'Anxious'],
  yellow: ['Ecstatic', 'Enthusiastic', 'Joyful', 'Excited', 'Happy'],
  blue: ['Lonely', 'Sad', 'Disappointed', 'Tired', 'Bored'],
  green: ['Calm', 'Peaceful', 'Relaxed', 'Content', 'Thoughtful'],
};

export default function EmotionWheelScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant } = route.params;

  const emotions = EMOTIONS[quadrant] || [];

  const selectEmotion = (emotion: string) => {
    navigation.navigate('Definition', { quadrant, emotion });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Velg følelsen som passer best</Text>
      <Text style={styles.subtitle}>Dra til siden for å se flere</Text>

      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.emotionList}
      >
        {emotions.map((emotion, index) => (
          <TouchableOpacity
            key={index}
            style={[styles.emotionCircle, { backgroundColor: getQuadrantColor(quadrant) }]}
            onPress={() => selectEmotion(emotion)}
          >
            <Text style={styles.emotionText}>{emotion}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <Text style={styles.note}>
        💡 Dette er en placeholder. Nyra vil designe 100 unike former (25 per kvadrant).
      </Text>
    </View>
  );
}

const getQuadrantColor = (quadrant: string) => {
  switch (quadrant) {
    case 'red': return '#FF6B6B';
    case 'yellow': return '#FFD93D';
    case 'blue': return '#6BCF7F';
    case 'green': return '#4ECDC4';
    default: return '#fff';
  }
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 14,
    color: '#aaa',
    textAlign: 'center',
    marginBottom: 40,
  },
  emotionList: {
    paddingHorizontal: 10,
    gap: 20,
  },
  emotionCircle: {
    width: 150,
    height: 150,
    borderRadius: 75,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emotionText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    textAlign: 'center',
  },
  note: {
    fontSize: 12,
    color: '#666',
    textAlign: 'center',
    marginTop: 40,
  },
});

