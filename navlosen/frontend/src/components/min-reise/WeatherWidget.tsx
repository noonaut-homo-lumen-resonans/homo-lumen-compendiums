"use client";

import { useState, useEffect } from "react";
import { Cloud, Sun, CloudRain, Wind, Droplet, Eye, AlertTriangle } from "lucide-react";

/**
 * WeatherWidget Component
 *
 * Displays environmental data that affects mood and energy:
 * - Temperature
 * - Weather conditions
 * - Sunlight/UV index
 * - Air quality
 * - Humidity
 *
 * For MVP: Uses mock data from localStorage
 * For Production: Can integrate with weather APIs (OpenWeather, Yr.no)
 */

interface WeatherData {
  temperature: number; // Celsius
  condition: "sunny" | "cloudy" | "rainy" | "windy" | "snowy";
  uvIndex: number; // 0-11+
  airQuality: {
    aqi: number; // Air Quality Index (0-500)
    level: "good" | "moderate" | "unhealthy" | "hazardous";
  };
  humidity: number; // percentage
  location: string;
  timestamp: number;
}

export default function WeatherWidget() {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load weather data from localStorage (mock for MVP)
    if (typeof window !== "undefined") {
      const savedData = localStorage.getItem("navlosen_weather_data");

      if (savedData) {
        setWeatherData(JSON.parse(savedData));
      } else {
        // Generate mock data for demo (Oslo autumn weather)
        const mockData: WeatherData = {
          temperature: 12,
          condition: "cloudy",
          uvIndex: 2,
          airQuality: {
            aqi: 42,
            level: "good",
          },
          humidity: 68,
          location: "Oslo",
          timestamp: Date.now(),
        };
        setWeatherData(mockData);
        localStorage.setItem("navlosen_weather_data", JSON.stringify(mockData));
      }

      setIsLoading(false);
    }
  }, []);

  const getWeatherIcon = (condition: string) => {
    switch (condition) {
      case "sunny": return <Sun className="h-12 w-12 text-yellow-500" />;
      case "cloudy": return <Cloud className="h-12 w-12 text-gray-500" />;
      case "rainy": return <CloudRain className="h-12 w-12 text-blue-500" />;
      case "windy": return <Wind className="h-12 w-12 text-cyan-500" />;
      default: return <Cloud className="h-12 w-12 text-gray-500" />;
    }
  };

  const getAirQualityColor = (level: string) => {
    switch (level) {
      case "good": return "text-green-600 bg-green-50";
      case "moderate": return "text-yellow-600 bg-yellow-50";
      case "unhealthy": return "text-orange-600 bg-orange-50";
      case "hazardous": return "text-red-600 bg-red-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  const getUVWarning = (uvIndex: number) => {
    if (uvIndex >= 8) return { level: "Meget høy", color: "text-red-600" };
    if (uvIndex >= 6) return { level: "Høy", color: "text-orange-600" };
    if (uvIndex >= 3) return { level: "Moderat", color: "text-yellow-600" };
    return { level: "Lav", color: "text-green-600" };
  };

  const getMoodImpact = (weather: WeatherData) => {
    // Simple heuristic for weather impact on mood
    const impacts = [];

    if (weather.condition === "sunny" && weather.uvIndex >= 3) {
      impacts.push({ icon: "☀️", text: "Sollys øker serotonin", positive: true });
    }

    if (weather.condition === "rainy" || weather.condition === "cloudy") {
      impacts.push({ icon: "☁️", text: "Begrenset dagslys kan senke energi", positive: false });
    }

    if (weather.airQuality.level === "good") {
      impacts.push({ icon: "🌬️", text: "God luftkvalitet støtter konsentrasjon", positive: true });
    }

    if (weather.humidity > 80) {
      impacts.push({ icon: "💧", text: "Høy luftfuktighet kan påvirke komfort", positive: false });
    }

    return impacts;
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

  if (!weatherData) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-dashed border-gray-300">
        <Cloud className="h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-xl font-bold text-gray-900 mb-2">Vær & Miljø</h3>
        <p className="text-sm text-gray-600 mb-4">
          Se hvordan været påvirker ditt humør og energi.
        </p>
        <button className="text-blue-600 font-medium text-sm hover:underline">
          Aktiver værdata →
        </button>
      </div>
    );
  }

  const uvWarning = getUVWarning(weatherData.uvIndex);
  const moodImpacts = getMoodImpact(weatherData);

  return (
    <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-sky-300">
      {/* Header */}
      <div className="mb-6">
        {getWeatherIcon(weatherData.condition)}
        <h3 className="text-xl font-bold text-gray-900 mb-1 mt-4">Vær & Miljø</h3>
        <p className="text-sm text-gray-600">{weatherData.location}</p>
      </div>

      {/* Temperature */}
      <div className="mb-6">
        <div className="text-4xl font-bold text-gray-900">{weatherData.temperature}°C</div>
        <div className="text-sm text-gray-600 capitalize">
          {weatherData.condition === "sunny" ? "Solfylt" :
           weatherData.condition === "cloudy" ? "Overskyet" :
           weatherData.condition === "rainy" ? "Regn" : "Vind"}
        </div>
      </div>

      {/* Environmental metrics */}
      <div className="space-y-3 mb-6">
        {/* UV Index */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Sun className="h-5 w-5 text-yellow-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">UV-indeks</div>
              <div className="text-xs text-gray-600">Solstyrke</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm font-semibold text-gray-900">{weatherData.uvIndex}</div>
            <div className={`text-xs font-medium ${uvWarning.color}`}>{uvWarning.level}</div>
          </div>
        </div>

        {/* Air Quality */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Wind className="h-5 w-5 text-cyan-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">Luftkvalitet</div>
              <div className="text-xs text-gray-600">AQI {weatherData.airQuality.aqi}</div>
            </div>
          </div>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAirQualityColor(weatherData.airQuality.level)}`}>
            {weatherData.airQuality.level === "good" ? "God" :
             weatherData.airQuality.level === "moderate" ? "Moderat" :
             weatherData.airQuality.level === "unhealthy" ? "Dårlig" : "Farlig"}
          </span>
        </div>

        {/* Humidity */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center gap-3">
            <Droplet className="h-5 w-5 text-blue-600" />
            <div>
              <div className="text-sm font-medium text-gray-900">Luftfuktighet</div>
              <div className="text-xs text-gray-600">Relativ fuktighet</div>
            </div>
          </div>
          <span className="text-sm font-semibold text-gray-900">{weatherData.humidity}%</span>
        </div>
      </div>

      {/* Mood Impact */}
      {moodImpacts.length > 0 && (
        <div className="p-3 bg-sky-50 rounded-lg border border-sky-100">
          <div className="flex items-start gap-2 mb-2">
            <Eye className="h-4 w-4 text-sky-600 mt-0.5" />
            <span className="text-xs font-semibold text-sky-900">Påvirkning på humør:</span>
          </div>
          <div className="space-y-1">
            {moodImpacts.map((impact, idx) => (
              <div key={idx} className="flex items-start gap-2">
                <span className="text-xs">{impact.icon}</span>
                <span className={`text-xs ${impact.positive ? "text-green-700" : "text-gray-700"}`}>
                  {impact.text}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action button */}
      <div className="mt-4 text-sky-600 font-medium text-sm">
        Se værvarsel →
      </div>
    </div>
  );
}
