/**
 * Supabase Client for Web Console
 *
 * Handles authentication and database operations for Homo Lumen OS
 * Falls back to mock mode if Supabase is not configured
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://dummy.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1bW15IiwiaWF0IjoxNjQ1MTk5NTAwfQ.dummy';

const isSupabaseConfigured = !!(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY );

if (!isSupabaseConfigured) {
  console.warn('⚠️ Supabase not configured. Using mock mode. Database operations will return mock data.');
}

export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey);

// Database Types
export interface User {
  id: string;
  email: string;
  role: 'admin' | 'agent' | 'user';
  created_at: string;
  updated_at: string;
}

export interface AgentSession {
  id: string;
  agent_id: string;
  user_id: string;
  session_data: Record<string, any>;
  started_at: string;
  ended_at?: string;
}

export interface SMKEntry {
  id: string;
  agent_id: string;
  entry_type: 'learning' | 'decision' | 'interaction' | 'error';
  content: string;
  metadata: Record<string, any>;
  created_at: string;
}

export interface SystemMetric {
  id: string;
  metric_name: string;
  metric_value: number;
  metadata: Record<string, any>;
  recorded_at: string;
}

// Auth helpers
export async function signIn(email: string, password: string) {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: signIn called');
    return { user: { id: 'mock-user', email }, session: null };
  }

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });

  if (error) throw error;
  return data;
}

export async function signOut() {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: signOut called');
    return;
  }

  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function getCurrentUser() {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: getCurrentUser called');
    return null;
  }

  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) throw error;
  return user;
}

// Database helpers
export async function createAgentSession(
  agentId: string,
  userId: string,
  sessionData: Record<string, any>
): Promise<AgentSession> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: createAgentSession called');
    return {
      id: `mock-session-${Date.now()}`,
      agent_id: agentId,
      user_id: userId,
      session_data: sessionData,
      started_at: new Date().toISOString()
    };
  }

  const { data, error } = await supabase
    .from('agent_sessions')
    .insert({
      agent_id: agentId,
      user_id: userId,
      session_data: sessionData,
      started_at: new Date().toISOString()
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

export async function endAgentSession(sessionId: string): Promise<void> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: endAgentSession called');
    return;
  }

  const { error } = await supabase
    .from('agent_sessions')
    .update({ ended_at: new Date().toISOString() })
    .eq('id', sessionId);

  if (error) throw error;
}

export async function logSMKEntry(entry: Omit<SMKEntry, 'id' | 'created_at'>): Promise<SMKEntry> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: logSMKEntry called');
    return {
      id: `mock-smk-${Date.now()}`,
      ...entry,
      created_at: new Date().toISOString()
    };
  }

  const { data, error } = await supabase
    .from('smk_entries')
    .insert({
      ...entry,
      created_at: new Date().toISOString()
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

export async function getSMKEntries(
  agentId?: string,
  limit: number = 50
): Promise<SMKEntry[]> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: getSMKEntries called');
    return [];
  }

  let query = supabase
    .from('smk_entries')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(limit);

  if (agentId) {
    query = query.eq('agent_id', agentId);
  }

  const { data, error } = await query;
  if (error) throw error;
  return data || [];
}

export async function recordMetric(
  metricName: string,
  metricValue: number,
  metadata: Record<string, any> = {}
): Promise<SystemMetric> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: recordMetric called');
    return {
      id: `mock-metric-${Date.now()}`,
      metric_name: metricName,
      metric_value: metricValue,
      metadata,
      recorded_at: new Date().toISOString()
    };
  }

  const { data, error } = await supabase
    .from('system_metrics')
    .insert({
      metric_name: metricName,
      metric_value: metricValue,
      metadata,
      recorded_at: new Date().toISOString()
    })
    .select()
    .single();

  if (error) throw error;
  return data;
}

export async function getMetrics(
  metricName?: string,
  limit: number = 100
): Promise<SystemMetric[]> {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: getMetrics called');
    return [];
  }

  let query = supabase
    .from('system_metrics')
    .select('*')
    .order('recorded_at', { ascending: false })
    .limit(limit);

  if (metricName) {
    query = query.eq('metric_name', metricName);
  }

  const { data, error } = await query;
  if (error) throw error;
  return data || [];
}

// Real-time subscriptions
export function subscribeToSMKEntries(
  callback: (entry: SMKEntry) => void,
  agentId?: string
) {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: subscribeToSMKEntries called');
    return () => {}; // Return empty unsubscribe function
  }

  const channel = supabase
    .channel('smk_entries')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'smk_entries',
        filter: agentId ? `agent_id=eq.${agentId}` : undefined
      },
      (payload) => {
        callback(payload.new as SMKEntry);
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}

export function subscribeToMetrics(
  callback: (metric: SystemMetric) => void,
  metricName?: string
) {
  if (!isSupabaseConfigured) {
    console.warn('Mock mode: subscribeToMetrics called');
    return () => {}; // Return empty unsubscribe function
  }

  const channel = supabase
    .channel('system_metrics')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'system_metrics',
        filter: metricName ? `metric_name=eq.${metricName}` : undefined
      },
      (payload) => {
        callback(payload.new as SystemMetric);
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}
