/**
 * Root Page - Redirect to Dashboard
 *
 * Automatically redirects all traffic from / to /dashboard
 * where the NAV-Losen landing page is located.
 *
 * @version 1.0
 * @date 2025-10-20
 */

import { redirect } from 'next/navigation';

export default function Home() {
  redirect('/dashboard');
}
