/**
 * NAV-LOSEN MVP - QUADRANT SCREEN (Mestringsside Fase 2)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #6)
 * Description: 4 quadrants selection (High/Low Energy × Pleasant/Unpleasant)
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');
const QUADRANT_SIZE = (width - 60) / 2;

export default function QuadrantScreen() {
  const navigation = useNavigation();

  const selectQuadrant = (quadrant: 'red' | 'yellow' | 'blue' | 'green') => {
    navigation.navigate('EmotionWheel', { quadrant });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hvordan føler du deg akkurat nå?</Text>
      <Text style={styles.subtitle}>Trykk på fargen som passer best</Text>

      <View style={styles.quadrantGrid}>
        {/* Red Quadrant: High Energy Unpleasant */}
        <TouchableOpacity
          style={styles.quadrant}
          onPress={() => selectQuadrant('red')}
        >
          <LinearGradient
            colors={['#FF1106', '#FFA98A']}
            style={styles.quadrantGradient}
          >
            <Text style={styles.quadrantLabel}>Høy Energi</Text>
            <Text style={styles.quadrantLabel}>Ubehagelig</Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Yellow Quadrant: High Energy Pleasant */}
        <TouchableOpacity
          style={styles.quadrant}
          onPress={() => selectQuadrant('yellow')}
        >
          <LinearGradient
            colors={['#FFD700', '#FFF4A3']}
            style={styles.quadrantGradient}
          >
            <Text style={[styles.quadrantLabel, styles.darkText]}>Høy Energi</Text>
            <Text style={[styles.quadrantLabel, styles.darkText]}>Behagelig</Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Blue Quadrant: Low Energy Unpleasant */}
        <TouchableOpacity
          style={styles.quadrant}
          onPress={() => selectQuadrant('blue')}
        >
          <LinearGradient
            colors={['#4169E1', '#87CEEB']}
            style={styles.quadrantGradient}
          >
            <Text style={styles.quadrantLabel}>Lav Energi</Text>
            <Text style={styles.quadrantLabel}>Ubehagelig</Text>
          </LinearGradient>
        </TouchableOpacity>

        {/* Green Quadrant: Low Energy Pleasant */}
        <TouchableOpacity
          style={styles.quadrant}
          onPress={() => selectQuadrant('green')}
        >
          <LinearGradient
            colors={['#00FF7F', '#98FB98']}
            style={styles.quadrantGradient}
          >
            <Text style={[styles.quadrantLabel, styles.darkText]}>Lav Energi</Text>
            <Text style={[styles.quadrantLabel, styles.darkText]}>Behagelig</Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
    textAlign: 'center',
    marginBottom: 40,
  },
  quadrantGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 20,
  },
  quadrant: {
    width: QUADRANT_SIZE,
    height: QUADRANT_SIZE,
    borderRadius: 20,
    overflow: 'hidden',
  },
  quadrantGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  quadrantLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
  },
  darkText: {
    color: '#000',
  },
});

