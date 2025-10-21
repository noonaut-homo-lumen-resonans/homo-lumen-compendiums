/**
 * Device Frame Component
 *
 * Renders realistic mobile device frames (iPhone, Samsung, iPad)
 * with authentic styling (notches, cameras, rounded corners).
 *
 * @version 1.0
 * @date 2025-10-21
 */

'use client';

import { useState } from 'react';

interface DeviceFrameProps {
  deviceType: 'iphone' | 'samsung' | 'ipad';
  iframeSrc: string;
}

export function DeviceFrame({ deviceType, iframeSrc }: DeviceFrameProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  // Device-specific dimensions and styles
  const deviceStyles = {
    iphone: {
      width: '393px',
      height: '852px',
      borderRadius: '47px',
      border: '12px solid #1d1d1f',
      backgroundColor: '#000',
    },
    samsung: {
      width: '360px',
      height: '780px',
      borderRadius: '40px',
      border: '10px solid #2c2c2c',
      backgroundColor: '#000',
    },
    ipad: {
      width: '820px',
      height: '1180px',
      borderRadius: '20px',
      border: '14px solid #5e5e5e',
      backgroundColor: '#000',
    },
  };

  const style = deviceStyles[deviceType];

  const handleIframeLoad = () => {
    setIsLoading(false);
    setHasError(false);
  };

  const handleIframeError = () => {
    setIsLoading(false);
    setHasError(true);
  };

  return (
    <div className="flex justify-center items-center py-8">
      <div
        className="relative shadow-2xl transition-all duration-500 ease-in-out"
        style={style}
      >
        {/* iPhone 15 Pro - Dynamic Island (Notch) */}
        {deviceType === 'iphone' && (
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-[120px] h-[30px] bg-[#1d1d1f] rounded-b-[20px] z-20" />
        )}

        {/* Samsung Galaxy S24 - Punch-hole camera */}
        {deviceType === 'samsung' && (
          <div className="absolute top-[20px] right-[30px] w-[10px] h-[10px] bg-[#1d1d1f] rounded-full z-20 shadow-inner" />
        )}

        {/* iframe Container */}
        <div className="relative w-full h-full overflow-hidden" style={{ borderRadius: `calc(${style.borderRadius} - 12px)` }}>
          {/* Loading Spinner */}
          {isLoading && !hasError && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-white z-10">
              <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mb-4" />
              <p className="text-gray-600 font-medium">Loading NAV-Losen...</p>
            </div>
          )}

          {/* Error State */}
          {hasError && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-red-50 z-10 p-8">
              <div className="text-6xl mb-4">⚠️</div>
              <h3 className="text-xl font-bold text-red-900 mb-2">
                Failed to Load Frontend
              </h3>
              <p className="text-sm text-red-700 text-center mb-4">
                Make sure NAV-Losen frontend is running on:
                <br />
                <code className="bg-red-100 px-2 py-1 rounded font-mono text-xs">
                  {iframeSrc.split('/',3).join('/')}
                </code>
              </p>
              <button
                onClick={() => {
                  setHasError(false);
                  setIsLoading(true);
                  // Force iframe reload
                  const iframe = document.querySelector('iframe');
                  if (iframe) iframe.src = iframe.src;
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Retry
              </button>
            </div>
          )}

          {/* Main iframe */}
          <iframe
            src={iframeSrc}
            className="w-full h-full border-0 bg-white"
            onLoad={handleIframeLoad}
            onError={handleIframeError}
            title="NAV-Losen Frontend"
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals allow-top-navigation"
            allow="fullscreen"
          />
        </div>

        {/* Device Buttons (decorative) */}
        {deviceType === 'iphone' && (
          <>
            {/* Power button (right side) */}
            <div className="absolute right-[-4px] top-[200px] w-[4px] h-[80px] bg-[#1d1d1f] rounded-r" />
            {/* Volume buttons (left side) */}
            <div className="absolute left-[-4px] top-[140px] w-[4px] h-[30px] bg-[#1d1d1f] rounded-l" />
            <div className="absolute left-[-4px] top-[185px] w-[4px] h-[30px] bg-[#1d1d1f] rounded-l" />
          </>
        )}

        {deviceType === 'samsung' && (
          <>
            {/* Power button (right side) */}
            <div className="absolute right-[-3px] top-[160px] w-[3px] h-[60px] bg-[#2c2c2c] rounded-r" />
            {/* Volume buttons (left side) */}
            <div className="absolute left-[-3px] top-[140px] w-[3px] h-[50px] bg-[#2c2c2c] rounded-l" />
          </>
        )}
      </div>
    </div>
  );
}
