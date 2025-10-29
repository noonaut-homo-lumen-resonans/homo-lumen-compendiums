"use client";

import { useState, useRef } from "react";
import { Camera, Upload, Mic, FileText, X, Check } from "lucide-react";
import Button from "@/components/ui/Button";

interface DocumentHelperProps {
  documentType?: string;
  onDocumentAdded?: (file: File, type: "upload" | "camera" | "voice") => void;
}

interface UploadedDocument {
  id: string;
  name: string;
  type: "upload" | "camera" | "voice";
  file: File;
  preview?: string;
  timestamp: Date;
}

/**
 * DocumentHelper Component
 *
 * Provides multiple ways to add documents to NAV applications:
 * - Upload files from device
 * - Take photos with camera
 * - Voice-to-text recording
 *
 * Triadisk Ethics:
 * ✅ Port 1 (Suverenitet): User chooses input method, can delete anytime
 * ✅ Port 2 (Koherens): Clear labels, predictable behavior
 * ✅ Port 3 (Healing): Reduces anxiety by offering multiple accessible options
 */
export default function DocumentHelper({
  documentType = "dokument",
  onDocumentAdded,
}: DocumentHelperProps) {
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Handle file upload
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    Array.from(files).forEach((file) => {
      const doc: UploadedDocument = {
        id: `upload-${Date.now()}-${Math.random()}`,
        name: file.name,
        type: "upload",
        file,
        timestamp: new Date(),
      };

      // Create preview for images/PDFs
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setDocuments((prev) => [
            ...prev,
            { ...doc, preview: e.target?.result as string },
          ]);
        };
        reader.readAsDataURL(file);
      } else {
        setDocuments((prev) => [...prev, doc]);
      }

      onDocumentAdded?.(file, "upload");
    });

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Handle camera capture
  const handleCameraCapture = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];
    const doc: UploadedDocument = {
      id: `camera-${Date.now()}`,
      name: `Bilde_${new Date().toLocaleString("nb-NO").replace(/[:.]/g, "-")}.jpg`,
      type: "camera",
      file,
      timestamp: new Date(),
    };

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setDocuments((prev) => [
        ...prev,
        { ...doc, preview: e.target?.result as string },
      ]);
    };
    reader.readAsDataURL(file);

    onDocumentAdded?.(file, "camera");

    // Reset input
    if (cameraInputRef.current) {
      cameraInputRef.current.value = "";
    }
  };

  // Handle voice recording
  const handleVoiceRecording = async () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
        mediaRecorderRef.current.stop();
      }
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
      setIsRecording(false);
      setRecordingTime(0);
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks: Blob[] = [];

        mediaRecorder.ondataavailable = (event) => {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          const audioFile = new File(
            [audioBlob],
            `Tale_${new Date().toLocaleString("nb-NO").replace(/[:.]/g, "-")}.webm`,
            { type: "audio/webm" }
          );

          const doc: UploadedDocument = {
            id: `voice-${Date.now()}`,
            name: audioFile.name,
            type: "voice",
            file: audioFile,
            timestamp: new Date(),
          };

          setDocuments((prev) => [...prev, doc]);
          onDocumentAdded?.(audioFile, "voice");

          // Stop all tracks
          stream.getTracks().forEach((track) => track.stop());
        };

        mediaRecorder.start();
        mediaRecorderRef.current = mediaRecorder;
        setIsRecording(true);

        // Start timer
        recordingIntervalRef.current = setInterval(() => {
          setRecordingTime((prev) => prev + 1);
        }, 1000);
      } catch (error) {
        console.error("Error accessing microphone:", error);
        alert(
          "Kunne ikke få tilgang til mikrofonen. Sjekk at du har gitt tillatelse i nettleseren."
        );
      }
    }
  };

  // Remove document
  const handleRemoveDocument = (id: string) => {
    setDocuments((prev) => prev.filter((doc) => doc.id !== id));
  };

  // Format recording time
  const formatRecordingTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="space-y-4">
      {/* Action Buttons */}
      <div className="flex flex-wrap gap-3">
        {/* Upload File */}
        <Button
          variant="secondary"
          size="medium"
          leftIcon={<Upload className="h-5 w-5 flex-shrink-0" />}
          onClick={() => fileInputRef.current?.click()}
        >
          Last opp dokument
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*,.pdf,.doc,.docx"
          multiple
          onChange={handleFileUpload}
          className="hidden"
          aria-label="Last opp dokument fra enhet"
        />

        {/* Take Photo */}
        <Button
          variant="secondary"
          size="medium"
          leftIcon={<Camera className="h-5 w-5 flex-shrink-0" />}
          onClick={() => cameraInputRef.current?.click()}
        >
          Ta bilde
        </Button>
        <input
          ref={cameraInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleCameraCapture}
          className="hidden"
          aria-label="Ta bilde av dokument"
        />

        {/* Voice Recording */}
        <Button
          variant={isRecording ? "destructive" : "secondary"}
          size="medium"
          leftIcon={<Mic className="h-5 w-5 flex-shrink-0" />}
          onClick={handleVoiceRecording}
        >
          {isRecording ? `Stopp (${formatRecordingTime(recordingTime)})` : "Snakk inn"}
        </Button>
      </div>

      {/* Uploaded Documents List */}
      {documents.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Lagrede dokumenter ({documents.length})
          </h3>
          <div className="space-y-2">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center gap-3 rounded-xl border border-gray-200 bg-white p-3"
              >
                {/* Icon/Preview */}
                <div className="flex-shrink-0">
                  {doc.preview ? (
                    <img
                      src={doc.preview}
                      alt={doc.name}
                      className="h-12 w-12 rounded object-cover"
                    />
                  ) : (
                    <div className="flex h-12 w-12 items-center justify-center rounded bg-blue-100">
                      {doc.type === "voice" ? (
                        <Mic className="h-6 w-6 text-blue-600" />
                      ) : (
                        <FileText className="h-6 w-6 text-blue-600" />
                      )}
                    </div>
                  )}
                </div>

                {/* Info */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-[var(--color-text-primary)] truncate">
                    {doc.name}
                  </p>
                  <p className="text-xs text-[var(--color-text-tertiary)]">
                    {doc.type === "upload" && "Opplastet"}
                    {doc.type === "camera" && "Fotografert"}
                    {doc.type === "voice" && "Taleopptak"} ·{" "}
                    {doc.timestamp.toLocaleTimeString("nb-NO", {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>

                {/* Status & Remove */}
                <div className="flex items-center gap-2">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-green-100">
                    <Check className="h-4 w-4 text-green-600" />
                  </div>
                  <button
                    onClick={() => handleRemoveDocument(doc.id)}
                    className="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 transition-colors hover:bg-gray-100 hover:text-red-600"
                    aria-label={`Fjern ${doc.name}`}
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Helper Text */}
      <p className="text-xs text-[var(--color-text-secondary)]">
        💡 Tips: Du kan laste opp flere dokumenter samtidig, eller bruke kameraet
        til å ta bilder av papirutskrifter.
      </p>
    </div>
  );
}
