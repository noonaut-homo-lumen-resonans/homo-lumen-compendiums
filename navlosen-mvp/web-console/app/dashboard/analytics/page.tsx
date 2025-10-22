/**
 * Analytics Dashboard Page
 *
 * Displays real-time analytics for Mobile Simulator usage.
 * Part of Day 4/7 implementation plan.
 *
 * Route: /dashboard/analytics
 *
 * @version 1.0
 * @date 2025-10-22
 */

import { AnalyticsDashboard } from '@/components/analytics/AnalyticsDashboard';

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <AnalyticsDashboard />
      </div>
    </div>
  );
}
