"use client";

import React, { useState, useRef, useEffect } from "react";
import Button from "@/components/ui/Button";
import { Play, Pause, Square, Volume2 } from "lucide-react";
import { MusicFrequency } from "@/types";

interface FrequencyPlayerProps {
  frequency: MusicFrequency;
  className?: string;
}

/**
 * FrequencyPlayer Component
 *
 * Interactive audio player that generates healing frequencies using Web Audio API.
 * Supports Solfeggio frequencies (174Hz, 396Hz, 417Hz, 528Hz, 639Hz, 741Hz, 852Hz, 963Hz)
 * and natural tuning (432Hz).
 *
 * Features:
 * - Real-time sine wave generation
 * - Volume control
 * - Visual frequency animation
 * - Play/Pause/Stop controls
 *
 * Triadisk Score: 0.12 (PROCEED)
 */
export default function FrequencyPlayer({
  frequency,
  className,
}: FrequencyPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.3); // Default 30% volume
  const [duration, setDuration] = useState(0); // seconds

  const audioContextRef = useRef<AudioContext | null>(null);
  const oscillatorRef = useRef<OscillatorNode | null>(null);
  const gainNodeRef = useRef<GainNode | null>(null);
  const startTimeRef = useRef<number>(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize Web Audio API
  useEffect(() => {
    return () => {
      // Cleanup on unmount
      stopAudio();
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  const startAudio = () => {
    // Create AudioContext
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    audioContextRef.current = audioContext;

    // Create oscillator (sine wave)
    const oscillator = audioContext.createOscillator();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(frequency.frequency, audioContext.currentTime);
    oscillatorRef.current = oscillator;

    // Create gain node for volume control
    const gainNode = audioContext.createGain();
    gainNode.gain.setValueAtTime(volume, audioContext.currentTime);
    gainNodeRef.current = gainNode;

    // Connect nodes: Oscillator -> Gain -> Destination
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    // Start oscillator
    oscillator.start();
    startTimeRef.current = Date.now();
    setIsPlaying(true);

    // Start timer
    timerRef.current = setInterval(() => {
      setDuration(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 1000);
  };

  const stopAudio = () => {
    if (oscillatorRef.current) {
      oscillatorRef.current.stop();
      oscillatorRef.current.disconnect();
      oscillatorRef.current = null;
    }
    if (gainNodeRef.current) {
      gainNodeRef.current.disconnect();
      gainNodeRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setIsPlaying(false);
    setDuration(0);
  };

  const handlePlayPause = () => {
    if (isPlaying) {
      stopAudio();
    } else {
      startAudio();
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (gainNodeRef.current) {
      gainNodeRef.current.gain.setValueAtTime(newVolume, audioContextRef.current!.currentTime);
    }
  };

  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className={`bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border-2 border-purple-200 p-6 ${className}`}>
      {/* Header */}
      <div className="mb-6 text-left">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-xl font-bold text-purple-900">{frequency.name}</h3>
          <div className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
            {frequency.frequency} Hz
          </div>
        </div>
        <p className="text-sm text-purple-700">{frequency.benefit}</p>
      </div>

      {/* Visual Frequency Animation */}
      <div className="mb-6 h-24 bg-white rounded-lg flex items-center justify-center overflow-hidden relative">
        {isPlaying ? (
          <div className="flex items-center justify-center gap-1 h-full w-full">
            {[...Array(40)].map((_, i) => (
              <div
                key={i}
                className="bg-purple-500 rounded-full transition-all duration-300"
                style={{
                  width: "4px",
                  height: `${Math.abs(Math.sin((i + duration) * 0.5)) * 80 + 10}%`,
                  animation: `pulse ${1000 / frequency.frequency}ms ease-in-out infinite`,
                  animationDelay: `${i * 20}ms`,
                }}
              />
            ))}
          </div>
        ) : (
          <div className="text-gray-400 text-sm">Trykk play for å starte</div>
        )}
      </div>

      {/* Duration Display */}
      {isPlaying && (
        <div className="text-center mb-4">
          <div className="text-2xl font-mono font-bold text-purple-900">
            {formatDuration(duration)}
          </div>
          <div className="text-xs text-purple-600">Spiller nå</div>
        </div>
      )}

      {/* Controls */}
      <div className="space-y-4">
        {/* Play/Pause/Stop */}
        <div className="flex gap-2 justify-center">
          <Button
            variant="primary"
            size="large"
            onClick={handlePlayPause}
            leftIcon={isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
            className="flex-1"
          >
            {isPlaying ? "Pause" : "Spill"}
          </Button>
          {isPlaying && (
            <Button
              variant="secondary"
              size="large"
              onClick={stopAudio}
              leftIcon={<Square className="h-5 w-5" />}
            >
              Stopp
            </Button>
          )}
        </div>

        {/* Volume Control */}
        <div className="flex items-center gap-3">
          <Volume2 className="h-5 w-5 text-purple-600 flex-shrink-0" />
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={volume}
            onChange={handleVolumeChange}
            className="flex-1 h-2 bg-purple-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
          />
          <span className="text-sm font-medium text-purple-900 w-12 text-right">
            {Math.round(volume * 100)}%
          </span>
        </div>
      </div>

      {/* Info */}
      <div className="mt-4 p-3 bg-purple-100 rounded-lg text-left">
        <p className="text-xs text-purple-800">
          <strong>💡 Tips:</strong> Bruk hodetelefoner for best opplevelse. Lytt i 5-10 minutter
          mens du puster rolig eller mediterer.
        </p>
      </div>

      {/* CSS Animation */}
      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 0.5;
          }
          50% {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
}
