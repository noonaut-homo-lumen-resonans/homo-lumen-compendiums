/**
 * NAV-LOSEN MVP - PRESSURE SIGNALS SCREEN (Mestringsside Fase 5)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #8)
 * Description: Check for pressure signals (inspired by How We Feel)
 */

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

// Pressure signal categories (based on polyvagal theory)
const PRESSURE_SIGNALS = [
  {
    id: 'physical',
    title: 'Fysiske signaler',
    signals: [
      'Hjertebank',
      'Tett i brystet',
      'Hodepine',
      'Muskelspenninger',
      'Mageproblemer',
      'Svimmelhet',
    ],
  },
  {
    id: 'emotional',
    title: 'Følelsesmessige signaler',
    signals: [
      'Irritabilitet',
      'Angst',
      'Tristhet',
      'Sinne',
      'Følelse av å være overveldmet',
      'Nummenhet',
    ],
  },
  {
    id: 'behavioral',
    title: 'Atferdsmessige signaler',
    signals: [
      'Isolasjon',
      'Prokrastinering',
      'Søvnproblemer',
      'Endret appetitt',
      'Unngåelse',
      'Hyperaktivitet',
    ],
  },
  {
    id: 'cognitive',
    title: 'Kognitive signaler',
    signals: [
      'Tankekjør',
      'Konsentrasjonsvansker',
      'Negative tanker',
      'Bekymringer',
      'Hukommelsesproblemer',
      'Beslutningsvansker',
    ],
  },
];

export default function PressureSignalsScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant, emotion } = route.params;
  const [selectedSignals, setSelectedSignals] = useState<string[]>([]);

  const toggleSignal = (signal: string) => {
    setSelectedSignals((prev) =>
      prev.includes(signal)
        ? prev.filter((s) => s !== signal)
        : [...prev, signal]
    );
  };

  const continueToChat = () => {
    navigation.navigate('LiraChat', {
      quadrant,
      emotion,
      pressureSignals: selectedSignals,
    });
  };

  const skipToChat = () => {
    navigation.navigate('LiraChat', {
      quadrant,
      emotion,
      pressureSignals: [],
    });
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Opplever du noen av disse signalene?</Text>
          <Text style={styles.subtitle}>
            Velg alle som passer. Dette hjelper oss å forstå deg bedre.
          </Text>
        </View>

        {PRESSURE_SIGNALS.map((category) => (
          <View key={category.id} style={styles.category}>
            <Text style={styles.categoryTitle}>{category.title}</Text>
            <View style={styles.signalGrid}>
              {category.signals.map((signal) => (
                <TouchableOpacity
                  key={signal}
                  style={[
                    styles.signalButton,
                    selectedSignals.includes(signal) && styles.signalButtonSelected,
                  ]}
                  onPress={() => toggleSignal(signal)}
                >
                  <Text
                    style={[
                      styles.signalText,
                      selectedSignals.includes(signal) && styles.signalTextSelected,
                    ]}
                  >
                    {signal}
                  </Text>
                  {selectedSignals.includes(signal) && (
                    <Text style={styles.checkmark}>✓</Text>
                  )}
                </TouchableOpacity>
              ))}
            </View>
          </View>
        ))}

        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            💡 Disse signalene er kroppens måte å kommunisere på. Det er helt normalt å oppleve dem.
          </Text>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.button, styles.primaryButton]}
          onPress={continueToChat}
        >
          <Text style={styles.buttonText}>
            Fortsett {selectedSignals.length > 0 && `(${selectedSignals.length} valgt)`}
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.secondaryButton]}
          onPress={skipToChat}
        >
          <Text style={[styles.buttonText, styles.secondaryButtonText]}>
            Hopp over
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    padding: 20,
    paddingTop: 40,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
    lineHeight: 22,
  },
  category: {
    padding: 20,
    paddingTop: 10,
  },
  categoryTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 15,
  },
  signalGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  signalButton: {
    backgroundColor: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  signalButtonSelected: {
    backgroundColor: '#4CAF50',
    borderColor: '#4CAF50',
  },
  signalText: {
    fontSize: 14,
    color: '#fff',
  },
  signalTextSelected: {
    fontWeight: '600',
  },
  checkmark: {
    fontSize: 14,
    color: '#fff',
    fontWeight: 'bold',
  },
  infoBox: {
    margin: 20,
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    padding: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  infoText: {
    fontSize: 14,
    color: '#aaa',
    lineHeight: 20,
  },
  footer: {
    padding: 20,
    paddingBottom: 30,
    gap: 12,
    borderTopWidth: 1,
    borderTopColor: '#1a1a1a',
  },
  button: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: '#4CAF50',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#333',
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  secondaryButtonText: {
    color: '#aaa',
  },
});

