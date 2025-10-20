/**
 * NAV-LOSEN MVP - SUPABASE CLIENT
 * Created: 20. oktober 2025
 * Author: Manus (Agent #6)
 * Description: Supabase client configuration for React Native
 */

import 'react-native-url-polyfill/auto';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';
import Constants from 'expo-constants';

// Get Supabase credentials from app.json extra config
const supabaseUrl = Constants.expoConfig?.extra?.supabaseUrl;
const supabaseAnonKey = Constants.expoConfig?.extra?.supabaseAnonKey;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase credentials in app.json');
}

// Create Supabase client with AsyncStorage for session persistence
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    storage: AsyncStorage,
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});

// ============================================================================
// AUTH HELPERS
// ============================================================================

/**
 * Sign up a new user
 */
export const signUp = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        pilot_group: 'tvedestrand',
      },
    },
  });

  if (error) throw error;
  return data;
};

/**
 * Sign in an existing user
 */
export const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) throw error;
  return data;
};

/**
 * Sign out the current user
 */
export const signOut = async () => {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
};

/**
 * Get the current user
 */
export const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) throw error;
  return user;
};

/**
 * Get the current session
 */
export const getSession = async () => {
  const { data: { session }, error } = await supabase.auth.getSession();
  if (error) throw error;
  return session;
};

// ============================================================================
// NAVLOSEN DATA HELPERS
// ============================================================================

/**
 * Create a new check-in
 */
export const createCheckin = async (checkinData: {
  quadrant: 'red' | 'yellow' | 'blue' | 'green';
  emotion_word: string;
  emotion_definition?: string;
  pressure_level?: number;
  body_signals?: string[];
  health_data?: {
    steps?: number;
    sleep_hours?: number;
    heart_rate?: number;
  };
}) => {
  const user = await getCurrentUser();
  if (!user) throw new Error('User not authenticated');

  const { data, error } = await supabase
    .from('navlosen_checkins')
    .insert({
      user_id: user.id,
      ...checkinData,
      body_signals: checkinData.body_signals ? JSON.stringify(checkinData.body_signals) : null,
      health_data: checkinData.health_data ? JSON.stringify(checkinData.health_data) : null,
    })
    .select()
    .single();

  if (error) throw error;
  return data;
};

/**
 * Get user's recent check-ins
 */
export const getRecentCheckins = async (limit: number = 10) => {
  const user = await getCurrentUser();
  if (!user) throw new Error('User not authenticated');

  const { data, error } = await supabase
    .from('navlosen_checkins')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })
    .limit(limit);

  if (error) throw error;
  return data;
};

/**
 * Create a new conversation with Lira
 */
export const createConversation = async (checkinId: string) => {
  const user = await getCurrentUser();
  if (!user) throw new Error('User not authenticated');

  const { data, error } = await supabase
    .from('navlosen_conversations')
    .insert({
      user_id: user.id,
      checkin_id: checkinId,
      status: 'active',
      messages: JSON.stringify([]),
    })
    .select()
    .single();

  if (error) throw error;
  return data;
};

/**
 * Add a message to a conversation
 */
export const addMessageToConversation = async (
  conversationId: string,
  message: {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
  }
) => {
  // Get current conversation
  const { data: conversation, error: fetchError } = await supabase
    .from('navlosen_conversations')
    .select('messages')
    .eq('id', conversationId)
    .single();

  if (fetchError) throw fetchError;

  // Parse existing messages
  const messages = JSON.parse(conversation.messages || '[]');
  messages.push(message);

  // Update conversation
  const { data, error } = await supabase
    .from('navlosen_conversations')
    .update({
      messages: JSON.stringify(messages),
      updated_at: new Date().toISOString(),
    })
    .eq('id', conversationId)
    .select()
    .single();

  if (error) throw error;
  return data;
};

/**
 * Get a conversation by ID
 */
export const getConversation = async (conversationId: string) => {
  const { data, error } = await supabase
    .from('navlosen_conversations')
    .select('*')
    .eq('id', conversationId)
    .single();

  if (error) throw error;
  return data;
};

/**
 * Add a recommendation
 */
export const addRecommendation = async (recommendationData: {
  conversation_id: string;
  recommendation_type: 'practice' | 'music' | 'resource';
  title: string;
  description?: string;
  content_url?: string;
}) => {
  const { data, error } = await supabase
    .from('navlosen_recommendations')
    .insert(recommendationData)
    .select()
    .single();

  if (error) throw error;
  return data;
};

/**
 * Get recommendations for a conversation
 */
export const getRecommendations = async (conversationId: string) => {
  const { data, error } = await supabase
    .from('navlosen_recommendations')
    .select('*')
    .eq('conversation_id', conversationId)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
};

/**
 * Add a mastery log entry
 */
export const addMasteryLogEntry = async (entryData: {
  strategy_title: string;
  strategy_description?: string;
  emotion_context?: string;
}) => {
  const user = await getCurrentUser();
  if (!user) throw new Error('User not authenticated');

  const { data, error } = await supabase
    .from('navlosen_mastery_log')
    .insert({
      user_id: user.id,
      ...entryData,
    })
    .select()
    .single();

  if (error) throw error;
  return data;
};

/**
 * Get user's mastery log
 */
export const getMasteryLog = async () => {
  const user = await getCurrentUser();
  if (!user) throw new Error('User not authenticated');

  const { data, error } = await supabase
    .from('navlosen_mastery_log')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
};

/**
 * Update mastery log entry effectiveness
 */
export const updateMasteryLogEffectiveness = async (
  entryId: string,
  effectivenessRating: number
) => {
  const { data, error } = await supabase
    .from('navlosen_mastery_log')
    .update({
      times_used: supabase.raw('times_used + 1'),
      effectiveness_rating: effectivenessRating,
      updated_at: new Date().toISOString(),
    })
    .eq('id', entryId)
    .select()
    .single();

  if (error) throw error;
  return data;
};

// ============================================================================
// REALTIME SUBSCRIPTIONS
// ============================================================================

/**
 * Subscribe to new recommendations for a conversation
 */
export const subscribeToRecommendations = (
  conversationId: string,
  callback: (payload: any) => void
) => {
  return supabase
    .channel(`recommendations:${conversationId}`)
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'navlosen_recommendations',
        filter: `conversation_id=eq.${conversationId}`,
      },
      callback
    )
    .subscribe();
};

/**
 * Unsubscribe from a channel
 */
export const unsubscribe = (channel: any) => {
  supabase.removeChannel(channel);
};

