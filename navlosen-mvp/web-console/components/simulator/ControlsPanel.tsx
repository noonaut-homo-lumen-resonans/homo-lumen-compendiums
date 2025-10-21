/**
 * Controls Panel Component
 *
 * Top panel with device selector, page navigation, and feature toggles
 * (Guided Tour, Screen Recording).
 *
 * @version 1.0
 * @date 2025-10-21
 */

'use client';

interface ControlsPanelProps {
  deviceType: 'iphone' | 'samsung' | 'ipad';
  onDeviceChange: (device: 'iphone' | 'samsung' | 'ipad') => void;
  currentPage: string;
  onPageChange: (page: string) => void;
  guidedTourActive: boolean;
  onGuidedTourToggle: () => void;
  recordingActive: boolean;
  onRecordingToggle: () => void;
}

const PAGES = [
  { path: '/', label: '🏠 Dashboard' },
  { path: '/mestring', label: '🧠 Mestring (HWF Emotion Wheel)' },
  { path: '/chatbot', label: '💚 Chatbot (Lira - QDA v2.0)' },
  { path: '/dokumenter', label: '📄 Dokumenter' },
  { path: '/forklar-brev', label: '📧 Forklar Brev (AI)' },
  { path: '/innstillinger', label: '⚙️ Innstillinger' },
  { path: '/jobb', label: '💼 Jobb (Arbeidsplassen.no)' },
  { path: '/min-reise', label: '🚀 Min Reise (Dashboard)' },
  { path: '/musikk', label: '🎵 Musikk (Healing Frequencies)' },
  { path: '/paminnelser', label: '⏰ Påminnelser' },
  { path: '/rettigheter', label: '⚖️ Rettigheter (NAV + Court Cases)' },
  { path: '/veiledninger', label: '📚 Veiledninger' },
  { path: '/ovelser/grounding-54321', label: '🧘 Grounding 5-4-3-2-1' },
  { path: '/ovelser/pust-468', label: '🌬️ Pust 4-6-8' },
];

export function ControlsPanel({
  deviceType,
  onDeviceChange,
  currentPage,
  onPageChange,
  guidedTourActive,
  onGuidedTourToggle,
  recordingActive,
  onRecordingToggle,
}: ControlsPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8 border border-gray-200">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Left Column: Device Selector */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            📱 Device Type
          </label>
          <select
            value={deviceType}
            onChange={(e) => onDeviceChange(e.target.value as any)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors bg-white"
          >
            <option value="iphone">iPhone 15 Pro (393×852)</option>
            <option value="samsung">Samsung Galaxy S24 (360×780)</option>
            <option value="ipad">iPad (820×1180)</option>
          </select>
        </div>

        {/* Middle Column: Page Navigation */}
        <div className="md:col-span-2">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            🗺️ Navigate to Page
          </label>
          <select
            value={currentPage}
            onChange={(e) => onPageChange(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors bg-white"
          >
            {PAGES.map((page) => (
              <option key={page.path} value={page.path}>
                {page.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Bottom Row: Feature Toggles */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex flex-wrap gap-3">
          {/* Guided Tour Toggle */}
          <button
            onClick={onGuidedTourToggle}
            disabled={true}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-500 rounded-lg cursor-not-allowed transition-colors"
            title="Coming in Dag 3"
          >
            <span className="text-lg">📖</span>
            <span className="font-medium">Guided Tour</span>
            <span className="text-xs bg-gray-300 px-2 py-0.5 rounded">Dag 3</span>
          </button>

          {/* Screen Recording Toggle */}
          <button
            onClick={onRecordingToggle}
            disabled={true}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-500 rounded-lg cursor-not-allowed transition-colors"
            title="Coming in Dag 5"
          >
            <span className="text-lg">⏺️</span>
            <span className="font-medium">Screen Recording</span>
            <span className="text-xs bg-gray-300 px-2 py-0.5 rounded">Dag 5</span>
          </button>

          {/* Analytics Dashboard Toggle */}
          <button
            disabled={true}
            className="flex items-center gap-2 px-4 py-2 bg-gray-200 text-gray-500 rounded-lg cursor-not-allowed transition-colors"
            title="Coming in Dag 4"
          >
            <span className="text-lg">📊</span>
            <span className="font-medium">Analytics</span>
            <span className="text-xs bg-gray-300 px-2 py-0.5 rounded">Dag 4</span>
          </button>

          {/* Info Badge */}
          <div className="ml-auto flex items-center gap-2 px-4 py-2 bg-blue-50 border border-blue-200 rounded-lg">
            <span className="text-sm text-blue-700 font-medium">
              Dag 1/7: Setup & Device Frame ✅
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
