import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Types for saved jobs
export interface SavedJob {
  id: string
  user_id: string
  job_id: string
  job_title: string | null
  company_name: string | null
  location: string | null
  saved_at: string
  notes: string | null
  application_status: 'not_applied' | 'applied' | 'interview' | 'rejected' | 'accepted'
  tags: string[] | null
  job_data: any | null
}

export interface JobAlert {
  id: string
  user_id: string
  name: string
  search_criteria: any
  frequency: 'realtime' | 'daily' | 'weekly'
  active: boolean
  last_sent_at: string | null
  created_at: string
  updated_at: string
}

export interface ApplicationHistory {
  id: string
  user_id: string
  job_id: string
  company: string | null
  position: string | null
  applied_at: string
  status: 'applied' | 'viewed' | 'interview_scheduled' | 'interview_completed' | 'rejected' | 'accepted' | 'withdrawn'
  notes: string | null
  interview_date: string | null
  response_date: string | null
  application_method: string | null
  email_thread_id: string | null
  created_at: string
  updated_at: string
}
