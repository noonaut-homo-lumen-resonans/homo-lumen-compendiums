"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import Button from "@/components/ui/Button";
import LiraContextPanel from "@/components/chatbot/LiraContextPanel";
import {
  MessageCircle,
  Send,
  User,
  RotateCcw,
  AlertCircle,
  ExternalLink,
  Camera,
  Upload,
  X as XIcon,
  Mic,
  MicOff,
  Heart,
} from "lucide-react";
import {
  sendToLira,
  loadBiofieldContext,
  type LiraMessage,
  type BiofieldContext,
} from "@/lib/liraService";

/**
 * Lira Chat Interface Component
 *
 * Empatisk chat-grensesnitt med Lira (GPT-4 via CSN Server)
 * som tilpasser seg brukerens emosjonelle tilstand fra Mestring.
 *
 * Features:
 * - Polyvagal-adaptive welcome messages + quick actions
 * - Multi-modal input: Text, voice (Web Speech API), image upload, camera capture
 * - Emotion sidebar with direct Mestring integration
 * - Message history with localStorage persistence
 * - Biofield context integration (stress, emotions, somatic signals)
 * - Auto-scroll, loading indicators, error handling
 * - AI disclaimer and "Snakk med veileder" link
 *
 * Triadisk Score: 0.2 (PROCEED)
 */
export default function ChatbotInterface() {
  // Message state
  const [messages, setMessages] = useState<LiraMessage[]>([]);
  const [input, setInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Image state
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [showCamera, setShowCamera] = useState<boolean>(false);

  // Voice input state
  const [isListening, setIsListening] = useState<boolean>(false);
  const [speechRecognition, setSpeechRecognition] = useState<any>(null);

  // Emotion sidebar state
  const [showEmotionSidebar, setShowEmotionSidebar] = useState<boolean>(false);

  // Biofield context (from Mestring if available)
  const [biofieldContext, setBiofieldContext] = useState<
    BiofieldContext | undefined
  >(undefined);

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Load biofield context and initialize speech recognition on mount
  useEffect(() => {
    const context = loadBiofieldContext();
    setBiofieldContext(context);

    // Initialize Speech Recognition (if supported)
    if (typeof window !== "undefined" && "webkitSpeechRecognition" in window) {
      const SpeechRecognition =
        (window as any).webkitSpeechRecognition ||
        (window as any).SpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "nb-NO"; // Norwegian

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      setSpeechRecognition(recognition);
    }
  }, []);

  // Load conversation history from localStorage
  useEffect(() => {
    if (typeof window === "undefined") return;

    const savedMessages = localStorage.getItem("navlosen-lira-history");
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        setMessages(parsed);
      } catch (error) {
        console.error("Failed to parse conversation history:", error);
      }
    } else {
      // Initialize with Lira's welcome message
      const welcomeMessage: LiraMessage = {
        role: "assistant",
        content: getWelcomeMessage(biofieldContext),
        timestamp: Date.now(),
      };
      setMessages([welcomeMessage]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Save conversation history to localStorage
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (messages.length === 0) return;

    localStorage.setItem("navlosen-lira-history", JSON.stringify(messages));
  }, [messages]);

  // Auto-scroll to bottom when messages change
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Get welcome message based on biofield context
  function getWelcomeMessage(context?: BiofieldContext): string {
    if (!context) {
      return "Hei, jeg er Lira. Jeg kan forklare begreper, foreslå neste steg og peke deg til riktige skjema. Jeg gir ikke juridiske råd, men jeg gjør det enklere å forstå valgene dine.";
    }

    const { polyvagalState, stressLevel } = context;

    if (polyvagalState === "dorsal") {
      return `Hei, jeg ser at du kanskje har hatt det litt vanskelig. Jeg er Lira, og jeg er her for deg. La oss ta det helt rolig. Hvordan har du det akkurat nå?`;
    }

    if (polyvagalState === "sympathetic") {
      return `Hei, jeg er Lira. Jeg ser at du kanskje er litt aktivert (stressnivå ${stressLevel}/10). Det er helt normalt. Jeg er her for å hjelpe deg - enten med NAV-spørsmål eller bare for å sjekke inn. Hva trenger du?`;
    }

    // Ventral (calm)
    return `Hei, jeg er Lira! Jeg ser at du har det ganske bra (stressnivå ${stressLevel}/10) - det er flott! Jeg kan hjelpe deg med NAV-spørsmål, eller vi kan bare snakke. Hva lurer du på?`;
  }

  // Get quick action buttons based on context
  const getQuickActions = (): string[] => {
    if (!biofieldContext) {
      // Default NAV-focused actions (from screenshot)
      return [
        "Forklar 'vedtak' i klarspråk",
        "Hva gjør jeg nå?",
        "Finn skjema for dagpenger",
        "Hvordan kontakter jeg en menneskelig veileder?",
      ];
    }

    const { polyvagalState } = biofieldContext;

    if (polyvagalState === "dorsal") {
      // High stress: Safety-focused
      return [
        "Jeg føler meg overveldet",
        "Jeg trenger trygghet",
        "Vis meg grounding-øvelse",
        "Snakk med veileder",
      ];
    }

    if (polyvagalState === "sympathetic") {
      // Medium stress: Action-focused
      return [
        "Hva gjør jeg nå?",
        "Vis meg puste-øvelse",
        "Finn skjema for dagpenger",
        "Hjelp meg forstå NAV",
      ];
    }

    // Ventral (calm): Exploration-focused
    return [
      "Fortell meg om NAV-ytelser",
      "Hva er mine rettigheter?",
      "Finn skjema for dagpenger",
      "Hvordan fungerer søknadsprosessen?",
    ];
  };

  const quickActions = getQuickActions();

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      alert("Vennligst last opp et bilde (JPG, PNG, etc.)");
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert("Bildet er for stort. Maksimal størrelse er 10MB.");
      return;
    }

    // Convert to base64
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = reader.result as string;
      setSelectedImage(base64);
    };
    reader.readAsDataURL(file);
  };

  // Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }, // Prefer back camera on mobile
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setShowCamera(true);
      }
    } catch (error) {
      console.error("Failed to start camera:", error);
      alert(
        "Kunne ikke starte kameraet. Sjekk at du har gitt tillatelse til kamera."
      );
    }
  };

  // Capture photo from camera
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");

    if (!context) return;

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0);

    // Convert to base64
    const base64 = canvas.toDataURL("image/jpeg", 0.8);
    setSelectedImage(base64);

    // Stop camera
    stopCamera();
  };

  // Stop camera
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
    setShowCamera(false);
  };

  // Remove selected image
  const removeImage = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Handle sending message (with optional image)
  const handleSend = async (predefinedMessage?: string) => {
    const messageToSend = predefinedMessage || input.trim();
    if (!messageToSend && !selectedImage) return;

    // Add user message
    const userMessage: LiraMessage = {
      role: "user",
      content: messageToSend || "📷 [Bilde lastet opp]",
      timestamp: Date.now(),
      imageUrl: selectedImage || undefined,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Send to Lira via CSN Server
      const response = await sendToLira(
        messageToSend || "Kan du hjelpe meg å forstå dette bildet?",
        messages,
        biofieldContext,
        selectedImage || undefined
      );

      // Add Lira's response
      const liraMessage: LiraMessage = {
        role: "assistant",
        content: response.message,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, liraMessage]);

      // Update Mestring timestamp if context was used
      if (biofieldContext) {
        localStorage.setItem(
          "navlosen-last-mestring-timestamp",
          Date.now().toString()
        );
      }

      // Clear image after sending
      setSelectedImage(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      console.error("Failed to send message to Lira:", error);

      // Add error message
      const errorMessage: LiraMessage = {
        role: "assistant",
        content:
          "Beklager, noe gikk galt. Prøv igjen, eller trykk 'Snakk med veileder' nedenfor for andre alternativer.",
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSend();
    }
  };

  // Handle reset conversation
  const handleReset = () => {
    if (
      !confirm(
        "Er du sikker på at du vil slette samtalehistorikken? Dette kan ikke angres."
      )
    ) {
      return;
    }

    localStorage.removeItem("navlosen-lira-history");
    const welcomeMessage: LiraMessage = {
      role: "assistant",
      content: getWelcomeMessage(biofieldContext),
      timestamp: Date.now(),
    };
    setMessages([welcomeMessage]);
  };

  // Toggle voice input (speech recognition)
  const toggleVoiceInput = () => {
    if (!speechRecognition) {
      alert(
        "Talegjenkjenning støttes ikke i denne nettleseren. Prøv Chrome eller Edge."
      );
      return;
    }

    if (isListening) {
      speechRecognition.stop();
      setIsListening(false);
    } else {
      speechRecognition.start();
      setIsListening(true);
    }
  };

  // Handle emotion selection from sidebar
  const handleEmotionSelect = (emotion: string) => {
    // Save emotion to localStorage for Mestring integration
    const existingEmotions = localStorage.getItem("navlosen-emotions");
    const emotions = existingEmotions ? JSON.parse(existingEmotions) : [];

    // Add new emotion if not already present
    const emotionExists = emotions.some((e: any) => e.word === emotion);
    if (!emotionExists) {
      emotions.push({ word: emotion, quadrant: getEmotionQuadrant(emotion) });
      localStorage.setItem("navlosen-emotions", JSON.stringify(emotions));
    }

    // Navigate to Mestring page (Stage 2 - Signals)
    localStorage.setItem("navlosen-mestring-stage", "signals");
    window.location.href = "/mestring";
  };

  // Get quadrant number for an emotion word
  const getEmotionQuadrant = (emotion: string): number => {
    const quadrantWords = {
      1: ["Gledelig", "Entusiastisk", "Inspirert", "Optimistisk", "Spent", "Energisk"],
      2: ["Rolig", "Takknemlig", "Trygg", "Tilfreds", "Fokusert", "Fredelig"],
      3: ["Trist", "Nedfor", "Utmattet", "Sårbar", "Ensom", "Nummen"],
      4: ["Frustrert", "Sint", "Irritert", "Engstelig", "Nervøs", "Overveldet", "Stresset", "Redd"],
    };

    for (const [quadrant, words] of Object.entries(quadrantWords)) {
      if (words.includes(emotion)) {
        return parseInt(quadrant);
      }
    }
    return 4; // Default to quadrant 4
  };

  return (
    <div className="flex gap-4">
      {/* Context Panel (Left Side) */}
      <LiraContextPanel biofieldContext={biofieldContext} />

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1 h-[calc(100vh-16rem)] bg-white rounded-lg shadow-lg">
        {/* Header */}
        <header className="p-4 border-b flex items-center justify-between bg-purple-50">
        <div className="flex items-center gap-3">
          <MessageCircle className="w-6 h-6 text-purple-500" />
          <div>
            <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
              Chat med Lira
            </h2>
            {biofieldContext && (
              <p className="text-xs text-[var(--color-text-secondary)]">
                Stressnivå: {biofieldContext.stressLevel}/10 (
                {biofieldContext.polyvagalState === "ventral"
                  ? "Rolig"
                  : biofieldContext.polyvagalState === "sympathetic"
                  ? "Aktivert"
                  : "Overveldet"}
                )
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEmotionSidebar(!showEmotionSidebar)}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            title="Følelser"
          >
            <Heart className="w-5 h-5" />
          </button>
          <button
            onClick={handleReset}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            title="Start ny samtale"
          >
            <RotateCcw className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-gray-50">
        {messages.map((msg, index) => (
          <div
            key={`${msg.timestamp}-${index}`}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`flex items-end max-w-[75%] ${
                msg.role === "user" ? "flex-row-reverse" : ""
              }`}
            >
              {/* Avatar */}
              {msg.role === "assistant" ? (
                <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center mr-2 mb-1 flex-shrink-0">
                  <MessageCircle className="w-5 h-5 text-purple-600" />
                </div>
              ) : (
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center ml-2 mb-1 flex-shrink-0">
                  <User className="w-5 h-5 text-blue-600" />
                </div>
              )}

              {/* Message bubble */}
              <div
                className={`p-3 rounded-xl ${
                  msg.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-white text-[var(--color-text-primary)] border border-gray-200"
                }`}
              >
                {/* Image preview (if attached) */}
                {msg.imageUrl && (
                  <img
                    src={msg.imageUrl}
                    alt="Uploaded image"
                    className="max-w-full rounded-lg mb-2 max-h-64 object-contain"
                  />
                )}

                <p className="whitespace-pre-wrap text-sm leading-relaxed">
                  {msg.content}
                </p>
                <p
                  className={`text-xs mt-1 ${
                    msg.role === "user"
                      ? "text-blue-100"
                      : "text-[var(--color-text-secondary)]"
                  }`}
                >
                  {new Date(msg.timestamp).toLocaleTimeString("nb-NO", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-end max-w-[75%]">
              <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center mr-2 mb-1 flex-shrink-0">
                <MessageCircle className="w-5 h-5 text-purple-600" />
              </div>
              <div className="p-3 rounded-xl bg-white border border-gray-200">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Camera Modal */}
      {showCamera && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Ta bilde</h3>
              <button
                onClick={stopCamera}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <XIcon className="w-5 h-5" />
              </button>
            </div>

            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full rounded-lg mb-4"
            />

            <div className="flex gap-2">
              <Button
                onClick={capturePhoto}
                variant="primary"
                size="large"
                leftIcon={<Camera className="w-5 h-5" />}
              >
                Ta bilde
              </Button>
              <Button onClick={stopCamera} variant="secondary" size="large">
                Avbryt
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Hidden canvas for camera capture */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Input area */}
      <div className="p-4 border-t bg-white">
        {/* Quick actions */}
        <div className="flex flex-wrap gap-2 mb-3">
          {quickActions.map((action) => (
            <button
              key={action}
              onClick={() => handleSend(action)}
              disabled={isLoading}
              className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {action}
            </button>
          ))}
        </div>

        {/* Image preview (if selected) */}
        {selectedImage && (
          <div className="mb-3 relative inline-block">
            <img
              src={selectedImage}
              alt="Selected image"
              className="max-h-32 rounded-lg border-2 border-purple-500"
            />
            <button
              onClick={removeImage}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
              title="Fjern bilde"
            >
              <XIcon className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Input field */}
        <div className="flex items-center gap-2">
          {/* Camera button */}
          <button
            onClick={startCamera}
            disabled={isLoading}
            className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Ta bilde"
          >
            <Camera className="w-5 h-5 text-gray-600" />
          </button>

          {/* File upload button */}
          <label
            className={`p-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer ${
              isLoading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            title="Last opp bilde"
          >
            <Upload className="w-5 h-5 text-gray-600" />
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              disabled={isLoading}
              className="hidden"
            />
          </label>

          {/* Voice input button */}
          <button
            onClick={toggleVoiceInput}
            disabled={isLoading}
            className={`p-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
              isListening ? "bg-red-100 border-red-500" : ""
            }`}
            title={isListening ? "Stopp lytting" : "Snakk"}
          >
            {isListening ? (
              <MicOff className="w-5 h-5 text-red-600 animate-pulse" />
            ) : (
              <Mic className="w-5 h-5 text-gray-600" />
            )}
          </button>

          <input
            ref={inputRef}
            type="text"
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent text-[var(--color-text-primary)] placeholder:text-[var(--color-text-secondary)]"
            placeholder="Skriv meldingen din her..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <Button
            onClick={() => handleSend()}
            disabled={isLoading || (!input.trim() && !selectedImage)}
            variant="primary"
            size="large"
            leftIcon={<Send className="w-5 h-5" />}
          >
            Send
          </Button>
        </div>

        {/* AI Disclaimer */}
        <div className="mt-3 p-3 bg-blue-50 border-l-4 border-blue-500 rounded-lg text-xs">
          <div className="flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-blue-800">
                <strong>AI-generert innhold:</strong> Jeg er en AI og kan gjøre
                feil. For personlig rådgivning og endelige svar, kontakt NAV
                direkte eller sjekk nav.no.
              </p>
              <a
                href="https://nav.no/kontakt"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 mt-2 text-blue-700 hover:text-blue-900 font-medium"
              >
                <ExternalLink className="w-3 h-3" />
                Snakk med veileder
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>

      {/* Emotion Sidebar (på høyre side) */}
      {showEmotionSidebar && (
        <div className="w-80 h-[calc(100vh-16rem)] bg-white rounded-lg shadow-lg p-4 overflow-y-auto">
          <div className="mb-4 pb-3 border-b">
            <h3 className="text-lg font-semibold text-[var(--color-text-primary)] flex items-center gap-2">
              <Heart className="w-5 h-5 text-red-500" />
              Følelser
            </h3>
            <p className="text-xs text-[var(--color-text-secondary)] mt-1">
              Klikk på en følelse → Gå direkte til Mestring
            </p>
          </div>

          {/* Dine valgte emosjoner (fra Mestring) */}
          {biofieldContext && biofieldContext.selectedEmotions && biofieldContext.selectedEmotions.length > 0 && (
            <div className="mb-4 p-3 bg-purple-50 border border-purple-200 rounded-lg">
              <h4 className="text-sm font-semibold text-purple-700 mb-2 flex items-center gap-2">
                ⭐ Dine valgte emosjoner
              </h4>
              <div className="flex flex-wrap gap-1">
                {biofieldContext.selectedEmotions.map((emotion, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 text-xs bg-white border-2 border-purple-400 text-purple-800 rounded-full font-medium"
                  >
                    {emotion.word}
                  </span>
                ))}
              </div>
              <p className="text-xs text-purple-600 mt-2">
                Fra din siste Mestring-økt
              </p>
            </div>
          )}

          <p className="text-xs text-[var(--color-text-secondary)] mb-3 italic">
            Alle følelser (velg for å legge til):
          </p>

          {/* Quadrant 1: Positive + High Energy (Green) */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-green-700 mb-2">
              ✨ Positiv + Energisk
            </h4>
            <div className="flex flex-wrap gap-1">
              {["Gledelig", "Entusiastisk", "Inspirert", "Optimistisk", "Spent", "Energisk"].map((emotion) => (
                <button
                  key={emotion}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-2 py-1 text-xs bg-green-50 hover:bg-green-100 text-green-800 rounded-full border border-green-200 transition-colors"
                >
                  {emotion}
                </button>
              ))}
            </div>
          </div>

          {/* Quadrant 2: Positive + Low Energy (Blue) */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-blue-700 mb-2">
              🌊 Positiv + Rolig
            </h4>
            <div className="flex flex-wrap gap-1">
              {["Rolig", "Takknemlig", "Trygg", "Tilfreds", "Fokusert", "Fredelig"].map((emotion) => (
                <button
                  key={emotion}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-2 py-1 text-xs bg-blue-50 hover:bg-blue-100 text-blue-800 rounded-full border border-blue-200 transition-colors"
                >
                  {emotion}
                </button>
              ))}
            </div>
          </div>

          {/* Quadrant 3: Negative + Low Energy (Gray) */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">
              💧 Negativ + Utmattet
            </h4>
            <div className="flex flex-wrap gap-1">
              {["Trist", "Nedfor", "Utmattet", "Sårbar", "Ensom", "Nummen"].map((emotion) => (
                <button
                  key={emotion}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-2 py-1 text-xs bg-gray-50 hover:bg-gray-100 text-gray-800 rounded-full border border-gray-300 transition-colors"
                >
                  {emotion}
                </button>
              ))}
            </div>
          </div>

          {/* Quadrant 4: Negative + High Energy (Orange) */}
          <div className="mb-4">
            <h4 className="text-sm font-semibold text-orange-700 mb-2">
              🔥 Negativ + Aktivert
            </h4>
            <div className="flex flex-wrap gap-1">
              {["Frustrert", "Sint", "Irritert", "Engstelig", "Nervøs", "Overveldet", "Stresset", "Redd"].map((emotion) => (
                <button
                  key={emotion}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-2 py-1 text-xs bg-orange-50 hover:bg-orange-100 text-orange-800 rounded-full border border-orange-200 transition-colors"
                >
                  {emotion}
                </button>
              ))}
            </div>
          </div>

          {/* Info box */}
          <div className="mt-6 p-3 bg-purple-50 border border-purple-200 rounded-lg">
            <p className="text-xs text-purple-800">
              <strong>💡 Tips:</strong> Klikk på en følelse for å starte Mestring-flowet. Du blir tatt direkte til Steg 2 (Trykk & Signaler) med valgt følelse allerede registrert.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
