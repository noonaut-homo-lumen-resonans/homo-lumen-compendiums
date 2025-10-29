"use client";

import { useState, useEffect } from "react";
import { Activity, Moon, Footprints, Heart, TrendingUp, TrendingDown, Minus } from "lucide-react";

/**
 * HealthMetrics Component
 *
 * Displays wearable/health data:
 * - Sleep quality and duration
 * - Daily steps
 * - Heart Rate Variability (HRV)
 * - Resting heart rate
 *
 * For MVP: Uses mock data from localStorage
 * For Production: Can integrate with Google Fit, Apple Health, etc.
 */

interface HealthData {
  sleep: {
    hours: number;
    quality: "excellent" | "good" | "fair" | "poor";
    timestamp: number;
  };
  steps: {
    count: number;
    goal: number;
    timestamp: number;
  };
  hrv: {
    value: number; // ms (higher = better recovery)
    trend: "up" | "down" | "stable";
    timestamp: number;
  };
  heartRate: {
    resting: number; // bpm
    timestamp: number;
  };
}

export default function HealthMetrics() {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load health data from localStorage (mock for MVP)
    if (typeof window !== "undefined") {
      const savedData = localStorage.getItem("navlosen_health_metrics");

      if (savedData) {
        setHealthData(JSON.parse(savedData));
      } else {
        // Generate mock data for demo
        const mockData: HealthData = {
          sleep: {
            hours: 7.2,
            quality: "good",
            timestamp: Date.now(),
          },
          steps: {
            count: 8234,
            goal: 10000,
            timestamp: Date.now(),
          },
          hrv: {
            value: 58,
            trend: "up",
            timestamp: Date.now(),
          },
          heartRate: {
            resting: 62,
            timestamp: Date.now(),
          },
        };
        setHealthData(mockData);
        localStorage.setItem("navlosen_health_metrics", JSON.stringify(mockData));
      }

      setIsLoading(false);
    }
  }, []);

  const getSleepQualityColor = (quality: string) => {
    switch (quality) {
      case "excellent": return "text-green-600 bg-green-50";
      case "good": return "text-blue-600 bg-blue-50";
      case "fair": return "text-yellow-600 bg-yellow-50";
      case "poor": return "text-red-600 bg-red-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  const getHRVTrendIcon = (trend: string) => {
    switch (trend) {
      case "up": return <TrendingUp className="h-4 w-4 text-green-600" />;
      case "down": return <TrendingDown className="h-4 w-4 text-red-600" />;
      case "stable": return <Minus className="h-4 w-4 text-gray-600" />;
      default: return null;
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg">
        <div className="animate-pulse space-y-4">
          <div className="h-12 w-12 bg-gray-200 rounded-full"></div>
          <div className="h-6 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
        </div>
      </div>
    );
  }

  if (!healthData) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-dashed border-gray-300">
        <Activity className="h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-xl font-bold text-gray-900 mb-2">Helseinnsikt</h3>
        <p className="text-sm text-gray-600 mb-4">
          Koble til en wearable for å spore søvn, aktivitet og HRV.
        </p>
        <button className="text-blue-600 font-medium text-sm hover:underline">
          Koble til enhet →
        </button>
      </div>
    );
  }

  const stepsPercentage = Math.min((healthData.steps.count / healthData.steps.goal) * 100, 100);

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-teal-300">
      {/* Header */}
      <div className="mb-6">
        <Activity className="h-12 w-12 text-teal-600 mb-4" />
        <h3 className="text-xl font-bold text-gray-900 mb-2">Helseinnsikt</h3>
        <p className="text-sm text-gray-600">
          Dine biometriske data påvirker din emosjonelle tilstand
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="space-y-4">
        {/* Sleep */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Moon className="h-5 w-5 text-indigo-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">Søvn</div>
              <div className="text-xs text-gray-600">{healthData.sleep.hours} timer</div>
            </div>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSleepQualityColor(healthData.sleep.quality)}`}>
            {healthData.sleep.quality === "excellent" ? "Utmerket" :
             healthData.sleep.quality === "good" ? "God" :
             healthData.sleep.quality === "fair" ? "Ok" : "Dårlig"}
          </span>
        </div>

        {/* Steps */}
        <div className="p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <Footprints className="h-5 w-5 text-green-600" />
              <div>
                <div className="text-sm font-medium text-gray-900">Skritt</div>
                <div className="text-xs text-gray-600">
                  {healthData.steps.count.toLocaleString()} / {healthData.steps.goal.toLocaleString()}
                </div>
              </div>
            </div>
            <span className="text-sm font-semibold text-green-600">
              {Math.round(stepsPercentage)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-green-400 to-green-600 h-2 rounded-full transition-all"
              style={{ width: `${stepsPercentage}%` }}
            ></div>
          </div>
        </div>

        {/* HRV */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Heart className="h-5 w-5 text-red-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">HRV</div>
              <div className="text-xs text-gray-600">Hjerteratevariasjon</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold text-gray-900">{healthData.hrv.value} ms</span>
            {getHRVTrendIcon(healthData.hrv.trend)}
          </div>
        </div>

        {/* Resting Heart Rate */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Activity className="h-5 w-5 text-purple-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">Hvilepuls</div>
              <div className="text-xs text-gray-600">Målt i hvile</div>
            </div>
          </div>
          <span className="text-sm font-semibold text-gray-900">{healthData.heartRate.resting} bpm</span>
        </div>
      </div>

      {/* Info note */}
      <div className="mt-4 p-3 bg-teal-50 rounded-lg border border-teal-100">
        <p className="text-xs text-teal-800">
          💡 Dårlig søvn og lav HRV kan redusere din evne til å håndtere stress
        </p>
      </div>

      {/* Action button */}
      <div className="mt-4 text-teal-600 font-medium text-sm">
        Se detaljer →
      </div>
    </div>
  );
}
