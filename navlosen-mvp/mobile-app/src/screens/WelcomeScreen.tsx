/**
 * NAV-LOSEN MVP - WELCOME SCREEN (Mestringsside Fase 1)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #6)
 * Description: Welcome screen explaining what NAV-Losen will help with
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function WelcomeScreen() {
  const navigation = useNavigation();

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Velkommen! 🌿</Text>
      <Text style={styles.subtitle}>NAV-Losen vil hjelpe deg med:</Text>

      <View style={styles.featureList}>
        <View style={styles.featureItem}>
          <Text style={styles.featureIcon}>🎯</Text>
          <Text style={styles.featureText}>
            Finne de rette ordene for å beskrive dine følelser
          </Text>
        </View>

        <View style={styles.featureItem}>
          <Text style={styles.featureIcon}>🛠️</Text>
          <Text style={styles.featureText}>
            Finne strategier som hjelper deg å jobbe med dine følelser
          </Text>
        </View>

        <View style={styles.featureItem}>
          <Text style={styles.featureIcon}>📊</Text>
          <Text style={styles.featureText}>
            Identifisere mønstre gjennom daglig sporing
          </Text>
        </View>
      </View>

      <Text style={styles.description}>
        Dette er et trygt rom for deg å utforske hvordan du har det. All data er kryptert og tilhører deg.
      </Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate('Quadrant')}
      >
        <Text style={styles.buttonText}>Start check-in</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  content: {
    padding: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 20,
    color: '#aaa',
    marginBottom: 30,
  },
  featureList: {
    marginBottom: 30,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    backgroundColor: '#1a1a1a',
    padding: 15,
    borderRadius: 10,
  },
  featureIcon: {
    fontSize: 32,
    marginRight: 15,
  },
  featureText: {
    fontSize: 16,
    color: '#fff',
    flex: 1,
  },
  description: {
    fontSize: 14,
    color: '#888',
    lineHeight: 22,
    marginBottom: 40,
  },
  button: {
    backgroundColor: '#00ff00',
    padding: 20,
    borderRadius: 15,
    alignItems: 'center',
  },
  buttonText: {
    color: '#000',
    fontSize: 20,
    fontWeight: 'bold',
  },
});

