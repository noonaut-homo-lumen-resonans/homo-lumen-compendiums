/**
 * Example: React Native Integration for QDA v2.0
 *
 * Copy this logic to: mobile-app/src/screens/LiraChatScreen.tsx
 *
 * @version 2.0
 * @date 2025-10-20
 */

import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, ScrollView, ActivityIndicator } from 'react-native';

// Configuration
const WEB_CONSOLE_URL =
  __DEV__
    ? 'http://localhost:3000' // Local development
    : 'https://nav-losen-web-console.netlify.app'; // Production

// Types
interface Message {
  id: string;
  sender: 'user' | 'lira';
  text: string;
  timestamp: number;
  layers?: any[]; // QDA layers (optional, for debugging)
  cost?: number; // QDA cost (optional, for debugging)
}

interface QDAResponse {
  success: boolean;
  response: string;
  layers: any[];
  highest_layer_used: string;
  total_cost: number;
  total_time: number;
  complexity_score: number;
}

// Props (from React Navigation)
interface LiraChatScreenProps {
  route: {
    params?: {
      quadrant?: string;
      emotion?: string;
      emotionWords?: string[];
      pressureSignals?: string[];
      stressLevel?: number;
    };
  };
}

export default function LiraChatScreen({ route }: LiraChatScreenProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Add welcome message on mount
  useEffect(() => {
    const welcomeMessage: Message = {
      id: 'welcome',
      sender: 'lira',
      text: 'Hei! Jeg er Lira. Hvordan kan jeg hjelpe deg i dag? 💙',
      timestamp: Date.now(),
    };
    setMessages([welcomeMessage]);
  }, []);

  /**
   * Main function: Generate Lira response using QDA v2.0
   */
  const generateLiraResponse = async (userMessage: string): Promise<string> => {
    try {
      console.log('[QDA] Calling API with message:', userMessage);

      // Prepare request body
      const requestBody = {
        message: userMessage,
        context: {
          quadrant: route.params?.quadrant,
          emotion: route.params?.emotion,
          emotionWords: route.params?.emotionWords,
          pressureSignals: route.params?.pressureSignals,
          sessionHistory: messages
            .filter(m => m.sender === 'user' || m.sender === 'lira')
            .map(m => ({
              role: m.sender === 'user' ? 'user' : 'assistant',
              content: m.text,
              timestamp: m.timestamp,
            })),
        },
        userState: {
          stressLevel: route.params?.stressLevel ?? 5,
          polyvagalState: calculatePolyvagalState(),
          arousal: calculateArousal(),
          valence: calculateValence(),
        },
        sessionId: 'session-' + Date.now(), // TODO: Use real session ID
      };

      console.log('[QDA] Request body:', JSON.stringify(requestBody, null, 2));

      // Call QDA API
      const response = await fetch(`${WEB_CONSOLE_URL}/api/qda/respond`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data: QDAResponse = await response.json();

      console.log('[QDA] Response received');
      console.log('[QDA] Layers used:', data.layers.map(l => l.layer_name).join(' → '));
      console.log('[QDA] Highest layer:', data.highest_layer_used);
      console.log('[QDA] Cost:', data.total_cost);
      console.log('[QDA] Time:', data.total_time, 'ms');

      // Optional: Store layers and cost for debugging
      // You can show these in a debug panel or admin view
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.sender === 'lira') {
        lastMessage.layers = data.layers;
        lastMessage.cost = data.total_cost;
      }

      return data.response;
    } catch (error) {
      console.error('[QDA] Error calling API:', error);

      // Fallback to mock response if API fails
      console.warn('[QDA] Falling back to mock response');
      return generateMockResponse(userMessage);
    }
  };

  /**
   * Helper: Calculate polyvagal state from stress level
   */
  const calculatePolyvagalState = (): 'dorsal' | 'sympathetic' | 'ventral' => {
    const stressLevel = route.params?.stressLevel ?? 5;
    if (stressLevel >= 8) return 'dorsal'; // Shutdown
    if (stressLevel >= 5) return 'sympathetic'; // Fight/flight
    return 'ventral'; // Social engagement
  };

  /**
   * Helper: Calculate arousal from stress level
   */
  const calculateArousal = (): number => {
    const stressLevel = route.params?.stressLevel ?? 5;
    return stressLevel / 10.0; // Simple linear mapping
  };

  /**
   * Helper: Calculate valence from quadrant
   */
  const calculateValence = (): number => {
    const quadrant = route.params?.quadrant;
    if (quadrant?.includes('positivt')) return 0.5;
    if (quadrant?.includes('negativt')) return -0.5;
    return 0.0;
  };

  /**
   * Fallback: Mock response (used if QDA API fails)
   */
  const generateMockResponse = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();

    // Critical keywords
    if (
      lowerMessage.includes('selvmord') ||
      lowerMessage.includes('ta livet') ||
      lowerMessage.includes('suicide')
    ) {
      return (
        '🚨 Jeg ser at du har det veldig vanskelig akkurat nå. Vennligst kontakt:\n\n' +
        '- Mental Helse: 116 123\n' +
        '- Legevakt: 113\n' +
        '- NAV Krisehjelp: https://nav.no/krisehjelp\n\n' +
        'Du fortjener å få hjelp umiddelbart. 💙'
      );
    }

    // Stress keywords
    if (lowerMessage.includes('stress') || lowerMessage.includes('jobb')) {
      return (
        'Jeg hører at du føler deg stresset. Det er helt normalt å kjenne på stress i perioder.\n\n' +
        'Noen ting som kan hjelpe:\n' +
        '- Ta korte pauser (5-10 min hver time)\n' +
        '- Pusteøvelser (4-6-8 metoden)\n' +
        '- Snakk med noen du stoler på\n\n' +
        'Hvis stresset vedvarer, kan NAV Arbeidsrådgivning hjelpe: https://nav.no/arbeid/raadgivning\n\n' +
        'Hvordan går det med deg nå? 💙'
      );
    }

    // Default response
    return (
      'Takk for at du deler dette med meg. Jeg er her for å lytte og støtte deg.\n\n' +
      'Kan du fortelle meg litt mer om hvordan du har det? 💙'
    );
  };

  /**
   * Handle send message
   */
  const handleSend = async () => {
    if (!inputText.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: 'user-' + Date.now(),
      sender: 'user',
      text: inputText.trim(),
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Generate Lira response using QDA v2.0
      const liraResponseText = await generateLiraResponse(userMessage.text);

      // Add Lira message
      const liraMessage: Message = {
        id: 'lira-' + Date.now(),
        sender: 'lira',
        text: liraResponseText,
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, liraMessage]);
    } catch (error) {
      console.error('[LiraChat] Error generating response:', error);

      // Add error message
      const errorMessage: Message = {
        id: 'error-' + Date.now(),
        sender: 'lira',
        text: 'Beklager, jeg hadde problemer med å svare. Vennligst prøv igjen. 💙',
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, padding: 16, backgroundColor: '#F5F7FA' }}>
      {/* Chat messages */}
      <ScrollView style={{ flex: 1 }}>
        {messages.map(msg => (
          <View
            key={msg.id}
            style={{
              alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.sender === 'user' ? '#2196F3' : '#FFFFFF',
              padding: 12,
              borderRadius: 8,
              marginBottom: 8,
              maxWidth: '80%',
            }}
          >
            <Text
              style={{
                color: msg.sender === 'user' ? '#FFFFFF' : '#000000',
                fontSize: 16,
              }}
            >
              {msg.text}
            </Text>
            {/* Debug info (optional - remove in production) */}
            {__DEV__ && msg.cost !== undefined && (
              <Text style={{ fontSize: 12, color: '#999', marginTop: 4 }}>
                Cost: ${msg.cost.toFixed(5)} | Layers: {msg.layers?.length ?? 0}
              </Text>
            )}
          </View>
        ))}
        {isLoading && (
          <View style={{ alignSelf: 'flex-start', marginBottom: 8 }}>
            <ActivityIndicator size="small" color="#2196F3" />
          </View>
        )}
      </ScrollView>

      {/* Input */}
      <View style={{ flexDirection: 'row', marginTop: 8 }}>
        <TextInput
          style={{
            flex: 1,
            backgroundColor: '#FFFFFF',
            padding: 12,
            borderRadius: 8,
            fontSize: 16,
          }}
          placeholder="Skriv en melding..."
          value={inputText}
          onChangeText={setInputText}
          onSubmitEditing={handleSend}
          editable={!isLoading}
        />
        <Text
          onPress={handleSend}
          style={{
            marginLeft: 8,
            padding: 12,
            backgroundColor: isLoading ? '#CCCCCC' : '#2196F3',
            borderRadius: 8,
            color: '#FFFFFF',
            fontWeight: 'bold',
          }}
        >
          Send
        </Text>
      </View>
    </View>
  );
}
