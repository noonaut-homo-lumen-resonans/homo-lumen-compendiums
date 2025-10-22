/**
 * Analytics Dashboard Component
 *
 * Real-time analytics for Mobile Simulator usage.
 * Tracks sessions, page views, device types, and tour completions.
 *
 * Triadic Ethics:
 * - Port 1 (Suverenitet): Transparent data visibility
 * - Port 2 (Koherens): Data-driven decision making
 * - Port 3 (Healing): Identify user pain points
 *
 * @version 1.0
 * @date 2025-10-22
 */

'use client';

import { useEffect, useState } from 'react';

interface AnalyticsData {
  sessions: {
    total: number;
    activeToday: number;
    activeLast7Days: number;
    avgDuration: string;
  };
  pages: {
    path: string;
    label: string;
    views: number;
    avgTimeSpent: string;
  }[];
  devices: {
    type: string;
    count: number;
    percentage: number;
  }[];
  tours: {
    name: string;
    started: number;
    completed: number;
    completionRate: number;
  }[];
  timeline: {
    hour: string;
    sessions: number;
  }[];
}

export function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('7d');

  useEffect(() => {
    // Load analytics from localStorage
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = () => {
    setLoading(true);

    // Get analytics from localStorage (mock data for now)
    const storedAnalytics = localStorage.getItem('simulator-analytics');

    if (storedAnalytics) {
      setAnalytics(JSON.parse(storedAnalytics));
    } else {
      // Initialize with mock data
      setAnalytics({
        sessions: {
          total: 42,
          activeToday: 5,
          activeLast7Days: 18,
          avgDuration: '8m 32s',
        },
        pages: [
          { path: '/mestring', label: '🧠 Mestring', views: 156, avgTimeSpent: '3m 12s' },
          { path: '/chatbot', label: '💚 Chatbot', views: 98, avgTimeSpent: '5m 45s' },
          { path: '/min-reise', label: '🚀 Min Reise', views: 87, avgTimeSpent: '2m 30s' },
          { path: '/', label: '🏠 Dashboard', views: 76, avgTimeSpent: '1m 15s' },
          { path: '/musikk', label: '🎵 Musikk', views: 65, avgTimeSpent: '4m 20s' },
        ],
        devices: [
          { type: 'iPhone 15 Pro', count: 28, percentage: 67 },
          { type: 'Samsung Galaxy S24', count: 10, percentage: 24 },
          { type: 'iPad', count: 4, percentage: 9 },
        ],
        tours: [
          { name: 'Welcome to NAV-Losen', started: 24, completed: 18, completionRate: 75 },
          { name: 'Meet Lira', started: 16, completed: 14, completionRate: 87.5 },
          { name: 'Regulate Your Nervous System', started: 12, completed: 8, completionRate: 67 },
        ],
        timeline: [
          { hour: '00:00', sessions: 1 },
          { hour: '03:00', sessions: 0 },
          { hour: '06:00', sessions: 2 },
          { hour: '09:00', sessions: 8 },
          { hour: '12:00', sessions: 12 },
          { hour: '15:00', sessions: 9 },
          { hour: '18:00', sessions: 6 },
          { hour: '21:00', sessions: 4 },
        ],
      });
    }

    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No analytics data available yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
          <p className="text-gray-600 mt-1">Mobile Simulator Usage Metrics</p>
        </div>

        {/* Time Range Selector */}
        <div className="flex gap-2">
          {(['24h', '7d', '30d'] as const).map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                timeRange === range
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {range === '24h' ? 'Last 24h' : range === '7d' ? 'Last 7 days' : 'Last 30 days'}
            </button>
          ))}
        </div>
      </div>

      {/* Session Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Total Sessions"
          value={analytics.sessions.total.toString()}
          icon="📊"
          trend="+12%"
          trendUp={true}
        />
        <MetricCard
          title="Active Today"
          value={analytics.sessions.activeToday.toString()}
          icon="👥"
          trend="+3"
          trendUp={true}
        />
        <MetricCard
          title="Active (7d)"
          value={analytics.sessions.activeLast7Days.toString()}
          icon="📈"
          trend="+8"
          trendUp={true}
        />
        <MetricCard
          title="Avg Duration"
          value={analytics.sessions.avgDuration}
          icon="⏱️"
          trend="+45s"
          trendUp={true}
        />
      </div>

      {/* Most Visited Pages */}
      <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">📄 Most Visited Pages</h3>
        <div className="space-y-3">
          {analytics.pages.map((page, index) => (
            <div key={page.path} className="flex items-center gap-4">
              <div className="w-8 text-center font-bold text-gray-400">#{index + 1}</div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-medium text-gray-900">{page.label}</span>
                  <span className="text-sm text-gray-600">{page.views} views</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ width: `${(page.views / analytics.pages[0].views) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500">{page.avgTimeSpent}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Device Distribution */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📱 Device Distribution</h3>
          <div className="space-y-4">
            {analytics.devices.map((device) => (
              <div key={device.type}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-700">{device.type}</span>
                  <span className="text-sm text-gray-600">
                    {device.count} ({device.percentage}%)
                  </span>
                </div>
                <div className="bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-green-500 h-3 rounded-full"
                    style={{ width: `${device.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Tour Completion Rates */}
        <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📖 Tour Completion Rates</h3>
          <div className="space-y-4">
            {analytics.tours.map((tour) => (
              <div key={tour.name}>
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-gray-700 text-sm">{tour.name}</span>
                  <span className="text-sm text-gray-600">
                    {tour.completed}/{tour.started} ({tour.completionRate}%)
                  </span>
                </div>
                <div className="bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full ${
                      tour.completionRate >= 75
                        ? 'bg-green-500'
                        : tour.completionRate >= 50
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${tour.completionRate}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">⏰ Usage Timeline (Today)</h3>
        <div className="flex items-end gap-2 h-40">
          {analytics.timeline.map((point) => (
            <div key={point.hour} className="flex-1 flex flex-col items-center gap-2">
              <div className="flex-1 w-full flex items-end">
                <div
                  className="w-full bg-blue-500 rounded-t-md hover:bg-blue-600 transition-colors"
                  style={{ height: `${(point.sessions / 12) * 100}%` }}
                  title={`${point.hour}: ${point.sessions} sessions`}
                />
              </div>
              <span className="text-xs text-gray-500">{point.hour}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>📊 Analytics Info:</strong> All data is stored locally in browser localStorage. No data is sent to external servers.
          This follows Triadic Ethics Port 1 (Cognitive Sovereignty) - your data stays with you.
        </p>
      </div>
    </div>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  icon: string;
  trend: string;
  trendUp: boolean;
}

function MetricCard({ title, value, icon, trend, trendUp }: MetricCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        <span
          className={`text-xs font-medium ${
            trendUp ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {trendUp ? '↑' : '↓'} {trend}
        </span>
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="text-sm text-gray-600">{title}</div>
    </div>
  );
}
