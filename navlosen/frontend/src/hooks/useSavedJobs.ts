import { useState, useEffect } from 'react'
import { supabase, type SavedJob } from '@/lib/supabase'
import { useGoogleAuth } from '@/contexts/GoogleAuthContext'

export function useSavedJobs() {
  const { user } = useGoogleAuth()
  const [savedJobs, setSavedJobs] = useState<SavedJob[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Fetch saved jobs when user logs in
  useEffect(() => {
    if (user) {
      fetchSavedJobs()
    } else {
      setSavedJobs([])
    }
  }, [user])

  const fetchSavedJobs = async () => {
    if (!user) return

    try {
      setLoading(true)
      setError(null)

      const { data, error: supabaseError } = await supabase
        .from('saved_jobs')
        .select('*')
        .eq('user_id', user.id)
        .order('saved_at', { ascending: false })

      if (supabaseError) throw supabaseError

      setSavedJobs(data || [])
    } catch (err: any) {
      console.error('Error fetching saved jobs:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const saveJob = async (job: {
    jobId: string
    jobTitle: string
    companyName: string
    location: string
    jobData?: any
  }) => {
    if (!user) {
      // TODO: Store in localStorage for non-logged-in users
      alert('Vennligst logg inn for å lagre jobber')
      return false
    }

    try {
      setLoading(true)
      setError(null)

      const { data, error: supabaseError } = await supabase
        .from('saved_jobs')
        .insert([
          {
            user_id: user.id,
            job_id: job.jobId,
            job_title: job.jobTitle,
            company_name: job.companyName,
            location: job.location,
            job_data: job.jobData,
            application_status: 'not_applied',
          },
        ])
        .select()

      if (supabaseError) throw supabaseError

      // Refresh saved jobs
      await fetchSavedJobs()
      return true
    } catch (err: any) {
      console.error('Error saving job:', err)
      setError(err.message)

      // Check if it's a duplicate error
      if (err.message.includes('duplicate') || err.message.includes('unique')) {
        alert('Denne jobben er allerede lagret')
      } else {
        alert(`Kunne ikke lagre jobb: ${err.message}`)
      }
      return false
    } finally {
      setLoading(false)
    }
  }

  const unsaveJob = async (jobId: string) => {
    if (!user) return false

    try {
      setLoading(true)
      setError(null)

      const { error: supabaseError } = await supabase
        .from('saved_jobs')
        .delete()
        .eq('user_id', user.id)
        .eq('job_id', jobId)

      if (supabaseError) throw supabaseError

      // Refresh saved jobs
      await fetchSavedJobs()
      return true
    } catch (err: any) {
      console.error('Error unsaving job:', err)
      setError(err.message)
      return false
    } finally {
      setLoading(false)
    }
  }

  const isJobSaved = (jobId: string): boolean => {
    return savedJobs.some(job => job.job_id === jobId)
  }

  const updateApplicationStatus = async (
    jobId: string,
    status: 'not_applied' | 'applied' | 'interview' | 'rejected' | 'accepted'
  ) => {
    if (!user) return false

    try {
      setLoading(true)
      setError(null)

      const { error: supabaseError } = await supabase
        .from('saved_jobs')
        .update({ application_status: status })
        .eq('user_id', user.id)
        .eq('job_id', jobId)

      if (supabaseError) throw supabaseError

      // Refresh saved jobs
      await fetchSavedJobs()
      return true
    } catch (err: any) {
      console.error('Error updating application status:', err)
      setError(err.message)
      return false
    } finally {
      setLoading(false)
    }
  }

  return {
    savedJobs,
    loading,
    error,
    saveJob,
    unsaveJob,
    isJobSaved,
    updateApplicationStatus,
    refetch: fetchSavedJobs,
  }
}
