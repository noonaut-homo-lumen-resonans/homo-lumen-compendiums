/**
 * NAV-LOSEN MVP - LIRA CHAT SCREEN (Mestringsside Fase 6)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #8)
 * Description: Chat with Lira for empathetic support and guidance
 * 
 * UPDATED: Dag 5 - QDA v2.0 Integration
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { supabase } from '../services/supabase';
import { API_ENDPOINTS, FEATURES, TIMEOUTS } from '../config';

interface Message {
  id: string;
  role: 'user' | 'lira';
  content: string;
  timestamp: Date;
}

export default function LiraChatScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant, emotion, pressureSignals = [], stressLevel = 5 } = route.params;
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    // Initial greeting from Lira
    const greeting = generateGreeting();
    addMessage('lira', greeting);
  }, []);

  const generateGreeting = () => {
    const signalsText = pressureSignals.length > 0
      ? ` Jeg ser at du opplever ${pressureSignals.length} ulike signaler.`
      : '';
    
    return `Hei! Jeg er Lira, din empatiske følgesvenn. Jeg ser at du føler deg ${emotion.toLowerCase()}.${signalsText} Jeg er her for å lytte og støtte deg. Hva tenker du på akkurat nå?`;
  };

  const addMessage = (role: 'user' | 'lira', content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
    
    // Auto-scroll to bottom
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = inputText.trim();
    setInputText('');
    addMessage('user', userMessage);
    setIsTyping(true);

    try {
      const response = FEATURES.USE_QDA_API
        ? await generateQDAResponse(userMessage)
        : await generateMockResponse(userMessage);
      
      setTimeout(() => {
        addMessage('lira', response);
        setIsTyping(false);
      }, TIMEOUTS.FALLBACK_DELAY);
      
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage('lira', 'Beklager, jeg hadde problemer med å svare. Kan du prøve igjen?');
      setIsTyping(false);
    }
  };

  /**
   * QDA v2.0 API Integration
   * Calls Web Console /api/qda/respond endpoint
   */
  const generateQDAResponse = async (userMessage: string): Promise<string> => {
    try {
      // Calculate polyvagal state based on stress level
      const polyvagalState = calculatePolyvagalState(stressLevel);
      const arousal = calculateArousal(stressLevel);
      const valence = calculateValence(quadrant);

      // Build request payload
      const payload = {
        message: userMessage,
        context: {
          quadrant: quadrant,
          emotion: emotion,
          emotionWords: [],
          pressureSignals: pressureSignals,
          sessionHistory: messages.map(m => ({
            role: m.role === 'user' ? 'user' : 'assistant',
            content: m.content,
            timestamp: m.timestamp.getTime(),
          })),
        },
        userState: {
          stressLevel: stressLevel,
          polyvagalState: polyvagalState,
          arousal: arousal,
          valence: valence,
        },
      };

      if (FEATURES.ENABLE_DEBUG_LOGS) {
        console.log('[QDA] Request:', JSON.stringify(payload, null, 2));
      }

      // Call QDA API with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), TIMEOUTS.QDA_REQUEST);

      const response = await fetch(API_ENDPOINTS.QDA_RESPOND, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      if (FEATURES.ENABLE_DEBUG_LOGS) {
        console.log('[QDA] Response:', {
          layers: data.layers?.map((l: any) => l.layer_name),
          cost: data.total_cost,
          time: data.total_time,
          highest_layer: data.highest_layer_used,
        });
      }

      return data.response;
    } catch (error) {
      console.error('[QDA] Error:', error);
      // Fallback to mock response
      return generateMockResponse(userMessage);
    }
  };

  /**
   * Helper: Calculate polyvagal state from stress level
   */
  const calculatePolyvagalState = (stressLevel: number): 'dorsal' | 'sympathetic' | 'ventral' => {
    if (stressLevel >= 8) return 'dorsal';
    if (stressLevel >= 5) return 'sympathetic';
    return 'ventral';
  };

  /**
   * Helper: Calculate arousal from stress level
   */
  const calculateArousal = (stressLevel: number): number => {
    return stressLevel / 10.0; // Simple mapping: 0-10 → 0.0-1.0
  };

  /**
   * Helper: Calculate valence from quadrant
   */
  const calculateValence = (quadrant?: string): number => {
    if (!quadrant) return 0.0;
    if (quadrant.includes('positivt')) return 0.5;
    if (quadrant.includes('negativt')) return -0.5;
    return 0.0;
  };

  /**
   * Mock response (fallback)
   * Used when QDA API is unavailable or disabled
   */
  const generateMockResponse = async (userMessage: string): Promise<string> => {
    const responses = [
      'Jeg hører deg. Det høres ut som en utfordrende situasjon. Kan du fortelle meg mer om hva som skjer?',
      'Takk for at du deler dette med meg. Dine følelser er helt gyldige. Hva tror du ville hjelpe deg akkurat nå?',
      'Det er modige av deg å åpne deg. Jeg er her for deg. Hva er det viktigste for deg i denne situasjonen?',
      'Jeg forstår at dette er vanskelig. La oss ta det steg for steg. Hva føles mest overkommelig å begynne med?',
      'Dine følelser forteller deg noe viktig. Hva tror du kroppen din prøver å kommunisere?',
    ];
    
    // Simple keyword-based response selection
    const lowerMessage = userMessage.toLowerCase();
    if (lowerMessage.includes('hjelp') || lowerMessage.includes('råd')) {
      return 'Jeg skal gjøre mitt beste for å hjelpe. Basert på det du har fortalt, kan det være nyttig å prøve noen mestringsstrategier. Skal vi se på noen anbefalinger sammen?';
    }
    
    if (lowerMessage.includes('takk')) {
      return 'Det er jeg som takker for at du stoler på meg. Du gjør en fantastisk jobb med å ta vare på deg selv. Ønsker du å se noen anbefalinger for videre støtte?';
    }
    
    // Random empathetic response
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const goToRecommendations = () => {
    navigation.navigate('Recommendations', {
      quadrant,
      emotion,
      pressureSignals,
      chatSummary: messages.map(m => `${m.role}: ${m.content}`).join('\n'),
    });
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={90}
    >
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>Lira</Text>
          <Text style={styles.headerSubtitle}>Din empatiske følgesvenn</Text>
        </View>
        <TouchableOpacity
          style={styles.recommendationsButton}
          onPress={goToRecommendations}
        >
          <Text style={styles.recommendationsButtonText}>Se anbefalinger →</Text>
        </TouchableOpacity>
      </View>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map((message) => (
          <View
            key={message.id}
            style={[
              styles.messageBubble,
              message.role === 'user' ? styles.userBubble : styles.liraBubble,
            ]}
          >
            <Text
              style={[
                styles.messageText,
                message.role === 'user' ? styles.userText : styles.liraText,
              ]}
            >
              {message.content}
            </Text>
            <Text style={styles.timestamp}>
              {message.timestamp.toLocaleTimeString('no-NO', {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </Text>
          </View>
        ))}
        
        {isTyping && (
          <View style={[styles.messageBubble, styles.liraBubble]}>
            <Text style={styles.typingIndicator}>Lira skriver...</Text>
          </View>
        )}
      </ScrollView>

      {/* Input */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Skriv en melding..."
          placeholderTextColor="#666"
          multiline
          maxLength={500}
        />
        <TouchableOpacity
          style={[styles.sendButton, !inputText.trim() && styles.sendButtonDisabled]}
          onPress={sendMessage}
          disabled={!inputText.trim()}
        >
          <Text style={styles.sendButtonText}>Send</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 50,
    borderBottomWidth: 1,
    borderBottomColor: '#1a1a1a',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#aaa',
  },
  recommendationsButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
  },
  recommendationsButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#fff',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 20,
    gap: 12,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#4CAF50',
  },
  liraBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#1a1a1a',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: '#fff',
  },
  liraText: {
    color: '#fff',
  },
  timestamp: {
    fontSize: 11,
    color: '#999',
    marginTop: 4,
  },
  typingIndicator: {
    fontSize: 14,
    color: '#aaa',
    fontStyle: 'italic',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 12,
    borderTopWidth: 1,
    borderTopColor: '#1a1a1a',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    fontSize: 16,
    color: '#fff',
    maxHeight: 100,
  },
  sendButton: {
    backgroundColor: '#4CAF50',
    borderRadius: 20,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#333',
  },
  sendButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
});

