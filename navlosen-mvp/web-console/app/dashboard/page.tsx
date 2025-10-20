'use client';

import { useEffect, useState } from 'react';
import { AGENTS, AgentType, getAgentStatus } from '@/lib/mcp-broker';
import { getSMKEntries, getMetrics, SMKEntry, SystemMetric } from '@/lib/supabase';

interface AgentStatus {
  agent: AgentType;
  online: boolean;
  latency: number;
  lastSeen: string;
}

export default function DashboardPage() {
  const [agentStatuses, setAgentStatuses] = useState<AgentStatus[]>([]);
  const [recentSMK, setRecentSMK] = useState<SMKEntry[]>([]);
  const [metrics, setMetrics] = useState<SystemMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  async function loadDashboardData() {
    try {
      // Load agent statuses
      const statuses = await Promise.all(
        Object.keys(AGENTS).map(async (agentId) => {
          const status = await getAgentStatus(agentId as AgentType);
          return {
            agent: agentId as AgentType,
            ...status
          };
        })
      );
      setAgentStatuses(statuses);

      // Load recent SMK entries
      const smk = await getSMKEntries(undefined, 10);
      setRecentSMK(smk);

      // Load system metrics
      const systemMetrics = await getMetrics(undefined, 20);
      setMetrics(systemMetrics);

      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Laster Homo Lumen OS...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Homo Lumen OS
          </h1>
          <p className="text-gray-600">
            Web Console for Agent Coalition Management
          </p>
        </div>

        {/* Agent Status Grid */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Agent Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {agentStatuses.map((status) => {
              const agent = AGENTS[status.agent];
              return (
                <div
                  key={status.agent}
                  className="bg-white rounded-lg shadow p-6 border-l-4"
                  style={{
                    borderLeftColor: status.online ? '#10b981' : '#ef4444'
                  }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {agent.name}
                    </h3>
                    <span
                      className={`w-3 h-3 rounded-full ${
                        status.online ? 'bg-green-500' : 'bg-red-500'
                      }`}
                    ></span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">
                    {agent.description}
                  </p>
                  <div className="text-xs text-gray-500">
                    <div className="flex justify-between mb-1">
                      <span>Status:</span>
                      <span className="font-medium">
                        {status.online ? 'Online' : 'Offline'}
                      </span>
                    </div>
                    <div className="flex justify-between mb-1">
                      <span>Latency:</span>
                      <span className="font-medium">
                        {status.latency > 0 ? `${status.latency}ms` : 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Model:</span>
                      <span className="font-medium text-xs">
                        {agent.model}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* SMK Entries */}
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Recent SMK Entries
            </h2>
            <div className="bg-white rounded-lg shadow">
              {recentSMK.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  No SMK entries yet
                </div>
              ) : (
                <div className="divide-y divide-gray-200">
                  {recentSMK.map((entry) => (
                    <div key={entry.id} className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-medium text-gray-900">
                            {AGENTS[entry.agent_id as AgentType]?.name || entry.agent_id}
                          </span>
                          <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                            {entry.entry_type}
                          </span>
                        </div>
                        <span className="text-xs text-gray-500">
                          {new Date(entry.created_at).toLocaleTimeString('no-NO')}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {entry.content}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* System Metrics */}
          <div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              System Metrics
            </h2>
            <div className="bg-white rounded-lg shadow">
              {metrics.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  No metrics recorded yet
                </div>
              ) : (
                <div className="divide-y divide-gray-200">
                  {metrics.slice(0, 10).map((metric) => (
                    <div key={metric.id} className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {metric.metric_name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {new Date(metric.recorded_at).toLocaleString('no-NO')}
                          </p>
                        </div>
                        <span className="text-lg font-semibold text-blue-600">
                          {metric.metric_value}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors">
              View All SMK Entries
            </button>
            <button className="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-colors">
              Agent Configuration
            </button>
            <button className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-6 rounded-lg transition-colors">
              System Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

