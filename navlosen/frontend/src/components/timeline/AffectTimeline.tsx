"use client";

import React, { useState, useEffect } from "react";
import { LineChart, Line, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Clock, TrendingUp, Heart, Info } from "lucide-react";
import {
  processEmotionHistory,
  detectAffectiveSignatures,
  getTimelinePointsForRange,
  generateAutoInsights,
  type TimelinePoint,
  type AffectivePattern,
} from "@/utils/affectTimeline";

interface AffectTimelineProps {
  compact?: boolean; // If true, show mini version for Dashboard
}

/**
 * Affect-Memory Timeline - "Digitalt Hippocampus"
 *
 * Visualizes emotional history in Circumplex space (valence × arousal).
 * Shows patterns, insights, and episodic memory of user's affective journey.
 *
 * Design: Polyvagal-safe colors (green/orange/blue), calm aesthetics
 */
export default function AffectTimeline({ compact = false }: AffectTimelineProps) {
  const [timelinePoints, setTimelinePoints] = useState<TimelinePoint[]>([]);
  const [patterns, setPatterns] = useState<AffectivePattern[]>([]);
  const [timeRange, setTimeRange] = useState<7 | 30 | 0>(7); // 7 days, 30 days, or all time (0)
  const [showInsights, setShowInsights] = useState<boolean>(false);
  const [insights, setInsights] = useState<string[]>([]);

  // Load and process emotion history
  useEffect(() => {
    const points = processEmotionHistory();
    setTimelinePoints(points);

    // Detect patterns
    const detectedPatterns = detectAffectiveSignatures(points);
    setPatterns(detectedPatterns);

    // Generate insights
    const generatedInsights = generateAutoInsights(points);
    setInsights(generatedInsights);
  }, []);

  // Filter points by time range
  const filteredPoints = timeRange === 0
    ? timelinePoints
    : getTimelinePointsForRange(timelinePoints, timeRange * 24);

  // Prepare data for LineChart (valence over time)
  const valenceChartData = filteredPoints.map(p => ({
    timestamp: p.timestamp,
    date: new Date(p.timestamp).toLocaleDateString('nb-NO', { month: 'short', day: 'numeric' }),
    valence: p.valence,
    emotionWord: p.emotionWord,
  }));

  // Prepare data for ScatterChart (Circumplex: arousal × valence)
  const circomplexData = filteredPoints.map(p => ({
    valence: p.valence,
    arousal: p.arousal,
    emotionWord: p.emotionWord,
    quadrant: p.quadrant,
    timestamp: p.timestamp,
  }));

  // Get quadrant color
  const getQuadrantColor = (quadrant: 1 | 2 | 3 | 4) => {
    const colors = {
      1: "#10b981", // Green (Q1 - Pleasant High Energy)
      2: "#f97316", // Orange (Q2 - Unpleasant High Energy)
      3: "#ef4444", // Red (Q3 - Unpleasant Low Energy)
      4: "#3b82f6", // Blue (Q4 - Pleasant Low Energy)
    };
    return colors[quadrant];
  };

  if (timelinePoints.length === 0) {
    return (
      <div className="p-6 bg-gray-50 rounded-lg text-center">
        <Heart className="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p className="text-gray-600">Ingen emosjonelle data ennå.</p>
        <p className="text-sm text-gray-500 mt-2">Start med Mestring for å registrere dine følelser.</p>
      </div>
    );
  }

  // Compact version for Dashboard
  if (compact) {
    return (
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-800 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-purple-500" />
            Din følelsesreise (siste 7 dager)
          </h3>
        </div>

        <ResponsiveContainer width="100%" height={150}>
          <LineChart data={valenceChartData.slice(-7)}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="date" tick={{ fontSize: 10 }} />
            <YAxis domain={[-1, 1]} tick={{ fontSize: 10 }} />
            <Tooltip
              content={({ payload }) => {
                if (payload && payload.length > 0) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-white p-2 border border-gray-200 rounded shadow-sm text-xs">
                      <p className="font-semibold">{data.emotionWord}</p>
                      <p className="text-gray-600">Valens: {data.valence.toFixed(2)}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Line type="monotone" dataKey="valence" stroke="#8b5cf6" strokeWidth={2} dot={{ fill: "#8b5cf6", r: 3 }} />
          </LineChart>
        </ResponsiveContainer>

        <div className="mt-2 text-center">
          <a href="/min-reise" className="text-sm text-purple-600 hover:underline">
            Se hele historikken →
          </a>
        </div>
      </div>
    );
  }

  // Full version for Min Reise page
  return (
    <div className="space-y-6">
      {/* Header with time range selector */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <Heart className="w-7 h-7 text-purple-500" />
          Din Følelsesreise
        </h2>

        <div className="flex gap-2">
          <button
            onClick={() => setTimeRange(7)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              timeRange === 7 ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            7 dager
          </button>
          <button
            onClick={() => setTimeRange(30)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              timeRange === 30 ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            30 dager
          </button>
          <button
            onClick={() => setTimeRange(0)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              timeRange === 0 ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Alle
          </button>
        </div>
      </div>

      {/* Valence over time chart */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="font-semibold text-gray-800 mb-4">Emosjonell Valens Over Tid</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={valenceChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="date" />
            <YAxis domain={[-1, 1]} label={{ value: 'Valens', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              content={({ payload }) => {
                if (payload && payload.length > 0) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
                      <p className="font-semibold text-gray-800">{data.emotionWord}</p>
                      <p className="text-sm text-gray-600">Valens: {data.valence.toFixed(2)}</p>
                      <p className="text-xs text-gray-500">{data.date}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Line type="monotone" dataKey="valence" stroke="#8b5cf6" strokeWidth={3} dot={{ fill: "#8b5cf6", r: 4 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Circumplex scatter plot */}
      <div className="bg-white rounded-lg p-6 shadow-sm">
        <h3 className="font-semibold text-gray-800 mb-4">Circumplex-Kart (Arousal × Valens)</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" dataKey="valence" domain={[-1, 1]} label={{ value: 'Valens', position: 'insideBottom', offset: -5 }} />
            <YAxis type="number" dataKey="arousal" domain={[0, 1]} label={{ value: 'Arousal', angle: -90, position: 'insideLeft' }} />
            <Tooltip
              content={({ payload }) => {
                if (payload && payload.length > 0) {
                  const data = payload[0].payload as any;
                  return (
                    <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
                      <p className="font-semibold" style={{ color: getQuadrantColor(data.quadrant) }}>
                        {data.emotionWord}
                      </p>
                      <p className="text-xs text-gray-600">Valens: {data.valence.toFixed(2)}</p>
                      <p className="text-xs text-gray-600">Arousal: {data.arousal.toFixed(2)}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            {[1, 2, 3, 4].map(quadrant => (
              <Scatter
                key={quadrant}
                data={circomplexData.filter(d => d.quadrant === quadrant)}
                fill={getQuadrantColor(quadrant as 1 | 2 | 3 | 4)}
                name={`Q${quadrant}`}
              />
            ))}
            <Legend />
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Insights (toggleable) */}
      <div className="bg-purple-50 rounded-lg p-6">
        <button
          onClick={() => setShowInsights(!showInsights)}
          className="flex items-center gap-2 font-semibold text-purple-800 mb-3"
        >
          <Info className="w-5 h-5" />
          <span>Auto-Innsikter {showInsights ? '▼' : '►'}</span>
        </button>

        {showInsights && (
          <div className="space-y-2">
            {insights.map((insight, index) => (
              <p key={index} className="text-sm text-purple-900">
                • {insight}
              </p>
            ))}
          </div>
        )}
      </div>

      {/* Patterns detected */}
      {patterns.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <Clock className="w-5 h-5 text-gray-600" />
            Mønstre Detektert
          </h3>
          <div className="space-y-3">
            {patterns.map((pattern, index) => (
              <div
                key={index}
                className={`p-3 rounded-lg border-l-4 ${
                  pattern.severity === 'high'
                    ? 'border-red-500 bg-red-50'
                    : pattern.severity === 'medium'
                    ? 'border-orange-500 bg-orange-50'
                    : 'border-green-500 bg-green-50'
                }`}
              >
                <p className="text-sm font-medium text-gray-800">{pattern.description}</p>
                <p className="text-xs text-gray-600 mt-1">
                  Type: {pattern.type} | Periode: {new Date(pattern.startTime).toLocaleDateString('nb-NO')}
                  {pattern.endTime !== pattern.startTime && ` - ${new Date(pattern.endTime).toLocaleDateString('nb-NO')}`}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
