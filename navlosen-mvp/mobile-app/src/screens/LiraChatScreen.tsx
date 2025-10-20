/**
 * NAV-LOSEN MVP - LIRA CHAT SCREEN (Mestringsside Fase 6)
 * Created: 20. oktober 2025
 * Author: Manus (Agent #8)
 * Description: Chat with Lira for empathetic support and guidance
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

interface Message {
  id: string;
  role: 'user' | 'lira';
  content: string;
  timestamp: Date;
}

export default function LiraChatScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { quadrant, emotion, pressureSignals = [] } = route.params;
  
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
      // In MVP: Use mock response
      // In production: Call OpenAI API via Supabase Edge Function
      
      const response = await generateLiraResponse(userMessage);
      
      setTimeout(() => {
        addMessage('lira', response);
        setIsTyping(false);
      }, 1500);
      
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage('lira', 'Beklager, jeg hadde problemer med å svare. Kan du prøve igjen?');
      setIsTyping(false);
    }
  };

  const generateLiraResponse = async (userMessage: string): Promise<string> => {
    // Mock responses for MVP
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

