/**
 * NAV-LOSEN MVP - DEFINITION SCREEN (Mestringsside Fase 4)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #8)
 * Description: Show emotion definition and allow user to confirm or refine
 */

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

// Emotion definitions (placeholder - will be expanded with full 100 emotions)
const EMOTION_DEFINITIONS: Record<string, string> = {
  'Enraged': 'Ekstrem sinne som føles overveldende og vanskelig å kontrollere.',
  'Panicked': 'Intens frykt eller angst som gjør det vanskelig å tenke klart.',
  'Stressed': 'Følelse av press og belastning som gjør deg anspent.',
  'Furious': 'Veldig sint, ofte med et sterkt ønske om å reagere.',
  'Anxious': 'Urolig og bekymret for noe som kan skje.',
  'Ecstatic': 'Overveldende lykke og begeistring.',
  'Enthusiastic': 'Full av energi og positivitet.',
  'Joyful': 'Dyp glede og tilfredshet.',
  'Excited': 'Spent og forventningsfull på en positiv måte.',
  'Happy': 'Generell følelse av velvære og tilfredshet.',
  'Lonely': 'Følelse av å være alene og savne kontakt.',
  'Sad': 'Trist og nedfor, ofte uten spesifikk grunn.',
  'Disappointed': 'Skuffet over noe som ikke gikk som forventet.',
  'Tired': 'Utmattet, både fysisk og mentalt.',
  'Bored': 'Kjeder seg og mangler stimulering.',
  'Calm': 'Rolig og avslappet, uten stress.',
  'Peaceful': 'Indre ro og harmoni.',
  'Relaxed': 'Avslappet og komfortabel.',
  'Content': 'Fornøyd med situasjonen.',
  'Thoughtful': 'Ettertenksom og reflekterende.',
};

export default function DefinitionScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant, emotion } = route.params;
  const [confirmed, setConfirmed] = useState(false);

  const definition = EMOTION_DEFINITIONS[emotion] || 'Beskrivelse kommer snart...';

  const confirmEmotion = () => {
    setConfirmed(true);
    setTimeout(() => {
      navigation.navigate('PressureSignals', { quadrant, emotion });
    }, 500);
  };

  const refineEmotion = () => {
    navigation.goBack();
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        {/* Emotion Display */}
        <View style={[styles.emotionBadge, { backgroundColor: getQuadrantColor(quadrant) }]}>
          <Text style={styles.emotionName}>{emotion}</Text>
        </View>

        {/* Definition */}
        <View style={styles.definitionCard}>
          <Text style={styles.definitionTitle}>Dette betyr:</Text>
          <Text style={styles.definitionText}>{definition}</Text>
        </View>

        {/* Confirmation Question */}
        <View style={styles.questionCard}>
          <Text style={styles.questionText}>
            Stemmer dette med hvordan du føler deg nå?
          </Text>
        </View>

        {/* Action Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.confirmButton, confirmed && styles.confirmedButton]}
            onPress={confirmEmotion}
            disabled={confirmed}
          >
            <Text style={styles.buttonText}>
              {confirmed ? '✓ Bekreftet' : 'Ja, dette stemmer'}
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.refineButton]}
            onPress={refineEmotion}
          >
            <Text style={styles.buttonText}>Nei, velg en annen</Text>
          </TouchableOpacity>
        </View>

        {/* Helper Text */}
        <Text style={styles.helperText}>
          Det er helt greit å endre valget ditt. Følelser kan være komplekse.
        </Text>
      </View>
    </ScrollView>
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
  },
  content: {
    padding: 20,
    paddingTop: 40,
  },
  emotionBadge: {
    alignSelf: 'center',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    marginBottom: 30,
  },
  emotionName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#000',
    textAlign: 'center',
  },
  definitionCard: {
    backgroundColor: '#1a1a1a',
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
  },
  definitionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#aaa',
    marginBottom: 10,
  },
  definitionText: {
    fontSize: 18,
    color: '#fff',
    lineHeight: 26,
  },
  questionCard: {
    backgroundColor: '#1a1a1a',
    borderRadius: 15,
    padding: 20,
    marginBottom: 30,
  },
  questionText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#fff',
    textAlign: 'center',
  },
  buttonContainer: {
    gap: 15,
    marginBottom: 20,
  },
  button: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  confirmButton: {
    backgroundColor: '#4CAF50',
  },
  confirmedButton: {
    backgroundColor: '#2E7D32',
  },
  refineButton: {
    backgroundColor: '#333',
    borderWidth: 1,
    borderColor: '#555',
  },
  buttonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
  helperText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    fontStyle: 'italic',
    marginTop: 10,
  },
});

