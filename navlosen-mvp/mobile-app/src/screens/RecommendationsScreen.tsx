/**
 * NAV-LOSEN MVP - RECOMMENDATIONS SCREEN (Final Step)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #8)
 * Description: Show personalized recommendations based on user's emotional state
 */

import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView, Linking } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';

interface Recommendation {
  id: string;
  category: 'immediate' | 'professional' | 'resources' | 'selfcare';
  title: string;
  description: string;
  action?: {
    label: string;
    type: 'phone' | 'url' | 'internal';
    value: string;
  };
}

export default function RecommendationsScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant, emotion, pressureSignals = [] } = route.params;
  
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);

  useEffect(() => {
    generateRecommendations();
  }, []);

  const generateRecommendations = () => {
    // Generate personalized recommendations based on emotional state
    const recs: Recommendation[] = [];

    // High-energy negative emotions (red quadrant)
    if (quadrant === 'red') {
      recs.push({
        id: '1',
        category: 'immediate',
        title: 'Akutt støtte',
        description: 'Hvis du trenger å snakke med noen med en gang, er Mental Helse hjelpetelefon tilgjengelig.',
        action: {
          label: 'Ring 116 123',
          type: 'phone',
          value: '116123',
        },
      });
      
      recs.push({
        id: '2',
        category: 'selfcare',
        title: 'Rolig ned nervesystemet',
        description: 'Prøv dype pustøvelser eller en kort gåtur for å regulere stressnivået.',
        action: {
          label: 'Se pustøvelser',
          type: 'internal',
          value: 'breathing',
        },
      });
    }

    // Low-energy negative emotions (blue quadrant)
    if (quadrant === 'blue') {
      recs.push({
        id: '3',
        category: 'professional',
        title: 'Snakk med fastlegen',
        description: 'Vedvarende tristhet eller utmattelse kan være tegn på depresjon. Fastlegen kan hjelpe.',
        action: {
          label: 'Bestill time på Helsenorge',
          type: 'url',
          value: 'https://www.helsenorge.no',
        },
      });
      
      recs.push({
        id: '4',
        category: 'selfcare',
        title: 'Aktiver kroppen',
        description: 'Lett fysisk aktivitet kan hjelpe med å løfte humøret og energinivået.',
        action: {
          label: 'Se treningsforslag',
          type: 'internal',
          value: 'exercise',
        },
      });
    }

    // High-energy positive emotions (yellow quadrant)
    if (quadrant === 'yellow') {
      recs.push({
        id: '5',
        category: 'selfcare',
        title: 'Bevar energien',
        description: 'Bruk denne positive energien konstruktivt, men husk å ta pauser.',
        action: {
          label: 'Se energitips',
          type: 'internal',
          value: 'energy',
        },
      });
    }

    // Low-energy positive emotions (green quadrant)
    if (quadrant === 'green') {
      recs.push({
        id: '6',
        category: 'selfcare',
        title: 'Vedlikehold roen',
        description: 'Fortsett med det som fungerer. Mindfulness og refleksjon kan forsterke denne tilstanden.',
        action: {
          label: 'Se mindfulness-øvelser',
          type: 'internal',
          value: 'mindfulness',
        },
      });
    }

    // Always include NAV resources
    recs.push({
      id: '7',
      category: 'resources',
      title: 'NAV Tvedestrand',
      description: 'NAV kan hjelpe med økonomisk rådgivning, jobbsøking og andre tjenester.',
      action: {
        label: 'Kontakt NAV',
        type: 'url',
        value: 'https://www.nav.no/person/kontakt-oss/nb/skriv-til-oss',
      },
    });

    // Add pressure-signal specific recommendations
    if (pressureSignals.length > 3) {
      recs.push({
        id: '8',
        category: 'professional',
        title: 'Vurder profesjonell hjelp',
        description: 'Du opplever flere stresssignaler. Det kan være lurt å snakke med en psykolog eller terapeut.',
        action: {
          label: 'Finn psykolog',
          type: 'url',
          value: 'https://www.psykologforeningen.no/finn-psykolog',
        },
      });
    }

    setRecommendations(recs);
  };

  const handleAction = (action: Recommendation['action']) => {
    if (!action) return;

    switch (action.type) {
      case 'phone':
        Linking.openURL(`tel:${action.value}`);
        break;
      case 'url':
        Linking.openURL(action.value);
        break;
      case 'internal':
        // Navigate to internal resource
        console.log('Navigate to:', action.value);
        break;
    }
  };

  const getCategoryColor = (category: Recommendation['category']) => {
    switch (category) {
      case 'immediate': return '#FF6B6B';
      case 'professional': return '#4ECDC4';
      case 'resources': return '#FFD93D';
      case 'selfcare': return '#6BCF7F';
      default: return '#fff';
    }
  };

  const getCategoryLabel = (category: Recommendation['category']) => {
    switch (category) {
      case 'immediate': return 'Akutt';
      case 'professional': return 'Profesjonell hjelp';
      case 'resources': return 'Ressurser';
      case 'selfcare': return 'Egenomsorg';
      default: return '';
    }
  };

  const finishSession = () => {
    navigation.navigate('Welcome');
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Anbefalinger for deg</Text>
          <Text style={styles.subtitle}>
            Basert på at du føler deg {emotion.toLowerCase()} og {pressureSignals.length} stresssignaler.
          </Text>
        </View>

        {recommendations.map((rec) => (
          <View key={rec.id} style={styles.card}>
            <View
              style={[
                styles.categoryBadge,
                { backgroundColor: getCategoryColor(rec.category) },
              ]}
            >
              <Text style={styles.categoryText}>
                {getCategoryLabel(rec.category)}
              </Text>
            </View>
            
            <Text style={styles.cardTitle}>{rec.title}</Text>
            <Text style={styles.cardDescription}>{rec.description}</Text>
            
            {rec.action && (
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => handleAction(rec.action)}
              >
                <Text style={styles.actionButtonText}>{rec.action.label}</Text>
              </TouchableOpacity>
            )}
          </View>
        ))}

        <View style={styles.infoBox}>
          <Text style={styles.infoTitle}>💡 Husk</Text>
          <Text style={styles.infoText}>
            Disse anbefalingene er veiledende. Du kjenner deg selv best. Hvis du er i tvil, kontakt alltid helsepersonell.
          </Text>
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={styles.finishButton}
          onPress={finishSession}
        >
          <Text style={styles.finishButtonText}>Fullfør økt</Text>
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
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
    lineHeight: 22,
  },
  card: {
    backgroundColor: '#1a1a1a',
    margin: 20,
    marginTop: 10,
    padding: 20,
    borderRadius: 16,
  },
  categoryBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginBottom: 12,
  },
  categoryText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#000',
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  cardDescription: {
    fontSize: 16,
    color: '#aaa',
    lineHeight: 22,
    marginBottom: 16,
  },
  actionButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  actionButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  infoBox: {
    margin: 20,
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    padding: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 14,
    color: '#aaa',
    lineHeight: 20,
  },
  footer: {
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#1a1a1a',
  },
  finishButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  finishButtonText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
});

