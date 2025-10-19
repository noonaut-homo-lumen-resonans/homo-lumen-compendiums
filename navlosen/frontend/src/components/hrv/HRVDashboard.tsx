"use client";

import React, { useState, useEffect } from "react";
import { Activity, TrendingUp, TrendingDown, Minus, Heart, Info, RefreshCw } from "lucide-react";
import {
  getLatestHRVReading,
  getHRVReadings,
  getHRVStats,
  generateHRVReading,
  initializeMockHRV,
  type HRVReading,
  type HRVStats,
} from "@/utils/mockHRV";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

/**
 * HRV Dashboard Component
 *
 * Displays Heart Rate Variability (HRV) data in two modes:
 * - Compact: Mini widget for Dashboard (current reading only)
 * - Full: Complete HRV dashboard with trends, stats, and education
 *
 * HRV Metrics:
 * - RMSSD: Root Mean Square of Successive Differences (primary HRV metric)
 * - Heart Rate: Beats per minute
 * - Polyvagal State: Nervous system state (ventral/sympathetic/dorsal)
 * - Stress Index: 0-100 score (lower is better)
 *
 * Educational Focus:
 * - Explains what HRV is and why it matters
 * - Shows relationship between HRV and stress/well-being
 * - Demonstrates polyvagal theory in action
 * - Keeps explanations short (as per user preference)
 *
 * NOTE: All data is SIMULATED for demonstration purposes.
 * Clearly labeled as mock data to avoid misleading users.
 *
 * Triadisk Score: 0.14 (PROCEED) - Educational, transparent about simulation
 */

interface HRVDashboardProps {
  compact?: boolean;
}

export default function HRVDashboard({ compact = false }: HRVDashboardProps) {
  const [currentReading, setCurrentReading] = useState<HRVReading | null>(null);
  const [readings, setReadings] = useState<HRVReading[]>([]);
  const [stats, setStats] = useState<HRVStats | null>(null);
  const [showInfo, setShowInfo] = useState<boolean>(false);
  const [timeRange, setTimeRange] = useState<24 | 168>(24); // 24h or 7 days

  // Load data on mount
  useEffect(() => {
    initializeMockHRV();
    loadData();
  }, [timeRange]);

  const loadData = () => {
    const latest = getLatestHRVReading();
    setCurrentReading(latest);

    const recentReadings = getHRVReadings(timeRange);
    setReadings(recentReadings);

    const recentStats = getHRVStats(timeRange);
    setStats(recentStats);
  };

  const handleRefresh = () => {
    const newReading = generateHRVReading();
    setCurrentReading(newReading);
    loadData();
  };

  // Get color for polyvagal state
  const getStateColor = (state: 'ventral' | 'sympathetic' | 'dorsal') => {
    switch (state) {
      case 'ventral':
        return 'text-green-600 bg-green-50';
      case 'sympathetic':
        return 'text-orange-600 bg-orange-50';
      case 'dorsal':
        return 'text-red-600 bg-red-50';
    }
  };

  const getStateLabel = (state: 'ventral' | 'sympathetic' | 'dorsal') => {
    switch (state) {
      case 'ventral':
        return 'Ventral (Rolig)';
      case 'sympathetic':
        return 'Sympathetic (Aktivert)';
      case 'dorsal':
        return 'Dorsal (Nedregulert)';
    }
  };

  const getQualityColor = (quality: 'excellent' | 'good' | 'fair' | 'poor') => {
    switch (quality) {
      case 'excellent':
        return 'text-green-700 bg-green-100';
      case 'good':
        return 'text-blue-700 bg-blue-100';
      case 'fair':
        return 'text-yellow-700 bg-yellow-100';
      case 'poor':
        return 'text-red-700 bg-red-100';
    }
  };

  const getTrendIcon = (trend: 'improving' | 'stable' | 'declining') => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'stable':
        return <Minus className="h-4 w-4 text-gray-600" />;
      case 'declining':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
    }
  };

  if (!currentReading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6">
        <p className="text-gray-600">Laster HRV-data...</p>
      </div>
    );
  }

  // Compact mode for Dashboard
  if (compact) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-4 border-l-4 border-purple-400">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3 flex-1">
            <Activity className="h-6 w-6 text-purple-600" />
            <div>
              <h3 className="text-sm font-semibold text-gray-900">HRV (Simulert)</h3>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="text-2xl font-bold text-purple-600">{currentReading.rmssd}</span>
                <span className="text-xs text-gray-600">ms RMSSD</span>
              </div>
            </div>
          </div>

          <div className="text-right">
            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getQualityColor(currentReading.quality)}`}>
              {currentReading.quality}
            </span>
            <p className="text-xs text-gray-600 mt-1">{currentReading.heartRate} bpm</p>
          </div>
        </div>

        <div className="mt-3 flex items-center justify-between">
          <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getStateColor(currentReading.polyvagalState)}`}>
            {getStateLabel(currentReading.polyvagalState)}
          </span>

          <button
            onClick={handleRefresh}
            className="text-purple-600 hover:text-purple-700 text-xs font-medium flex items-center gap-1"
          >
            <RefreshCw className="h-3 w-3" />
            Oppdater
          </button>
        </div>
      </div>
    );
  }

  // Full mode
  const chartData = readings.map(r => ({
    time: new Date(r.timestamp).toLocaleTimeString('nb-NO', { hour: '2-digit', minute: '2-digit' }),
    rmssd: r.rmssd,
    hr: r.heartRate,
    stress: r.stressIndex,
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">HRV Oversikt</h2>
          <p className="text-sm text-gray-600 mt-1">Simulert data for læring og testing</p>
        </div>
        <button
          onClick={() => setShowInfo(!showInfo)}
          className="text-purple-600 hover:text-purple-700 flex items-center gap-2"
        >
          <Info className="h-5 w-5" />
          <span className="text-sm font-medium">Hva er HRV?</span>
        </button>
      </div>

      {/* Info Panel */}
      {showInfo && (
        <div className="bg-purple-50 border-l-4 border-purple-400 p-4 rounded-lg">
          <h3 className="font-semibold text-purple-900 mb-2">Om HRV (Heart Rate Variability)</h3>
          <p className="text-sm text-purple-800 mb-2">
            HRV måler variasjon i tiden mellom hjerteslag. <strong>Høyere HRV = bedre stressmestring.</strong>
          </p>
          <ul className="text-sm text-purple-800 space-y-1 ml-4">
            <li>• <strong>RMSSD:</strong> Hovedmålet for HRV (ms). Høyere er bedre.</li>
            <li>• <strong>Polyvagal tilstand:</strong> Reflekterer nervesystemets tilstand.</li>
            <li>• <strong>Stress Index:</strong> 0-100 skår (lavere er bedre).</li>
          </ul>
          <p className="text-xs text-purple-700 mt-3 italic">
            💡 Denne dataen er simulert for å vise hvordan HRV fungerer. I virkeligheten måles HRV med spesielle sensorer.
          </p>
        </div>
      )}

      {/* Current Reading Card */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg p-6 border-2 border-purple-200">
        <div className="flex items-start justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Nåværende måling</h3>
          <button
            onClick={handleRefresh}
            className="px-3 py-1 bg-purple-500 hover:bg-purple-600 text-white rounded-lg text-sm font-medium flex items-center gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Ny måling
          </button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-gray-600 uppercase mb-1">RMSSD</p>
            <p className="text-3xl font-bold text-purple-600">{currentReading.rmssd}</p>
            <p className="text-xs text-gray-600">ms</p>
          </div>

          <div>
            <p className="text-xs text-gray-600 uppercase mb-1">Puls</p>
            <p className="text-3xl font-bold text-blue-600">{currentReading.heartRate}</p>
            <p className="text-xs text-gray-600">bpm</p>
          </div>

          <div>
            <p className="text-xs text-gray-600 uppercase mb-1">Stress Index</p>
            <p className="text-3xl font-bold text-orange-600">{currentReading.stressIndex}</p>
            <p className="text-xs text-gray-600">/100</p>
          </div>

          <div>
            <p className="text-xs text-gray-600 uppercase mb-1">Kvalitet</p>
            <span className={`inline-flex items-center px-3 py-2 rounded-lg text-sm font-semibold ${getQualityColor(currentReading.quality)}`}>
              {currentReading.quality}
            </span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-purple-200">
          <p className="text-sm text-gray-700 mb-2">Polyvagal tilstand:</p>
          <span className={`inline-flex items-center gap-2 px-4 py-2 rounded-full font-medium ${getStateColor(currentReading.polyvagalState)}`}>
            <Heart className="h-4 w-4" />
            {getStateLabel(currentReading.polyvagalState)}
          </span>
        </div>
      </div>

      {/* Stats Card */}
      {stats && stats.readingsCount > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Statistikk</h3>
            <div className="flex gap-2">
              <button
                onClick={() => setTimeRange(24)}
                className={`px-3 py-1 rounded-lg text-sm font-medium ${
                  timeRange === 24
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                24t
              </button>
              <button
                onClick={() => setTimeRange(168)}
                className={`px-3 py-1 rounded-lg text-sm font-medium ${
                  timeRange === 168
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                7d
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div>
              <p className="text-xs text-gray-600 uppercase mb-1">Gjennomsnitt RMSSD</p>
              <p className="text-2xl font-bold text-purple-600">{stats.avgRmssd}</p>
              <p className="text-xs text-gray-600">ms</p>
            </div>

            <div>
              <p className="text-xs text-gray-600 uppercase mb-1">Gjennomsnitt Puls</p>
              <p className="text-2xl font-bold text-blue-600">{stats.avgHeartRate}</p>
              <p className="text-xs text-gray-600">bpm</p>
            </div>

            <div>
              <p className="text-xs text-gray-600 uppercase mb-1">Gjennomsnitt Stress</p>
              <p className="text-2xl font-bold text-orange-600">{stats.stressAverage}</p>
              <p className="text-xs text-gray-600">/100</p>
            </div>

            <div>
              <p className="text-xs text-gray-600 uppercase mb-1">Trend</p>
              <div className="flex items-center gap-2">
                {getTrendIcon(stats.trend)}
                <span className="text-sm font-semibold capitalize">{stats.trend}</span>
              </div>
            </div>
          </div>

          {/* Chart */}
          {chartData.length > 1 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-3">HRV over tid</h4>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="time"
                    tick={{ fontSize: 12 }}
                    interval="preserveStartEnd"
                  />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="rmssd"
                    stroke="#8b5cf6"
                    strokeWidth={2}
                    name="RMSSD (ms)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}

      {/* Educational Footer */}
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <p className="text-xs text-gray-600">
          <strong>Merk:</strong> Denne HRV-dataen er simulert for læring og testing. For ekte HRV-måling, bruk enheter som Polar H10, Apple Watch med HRV-app, eller Oura Ring.
        </p>
      </div>
    </div>
  );
}
