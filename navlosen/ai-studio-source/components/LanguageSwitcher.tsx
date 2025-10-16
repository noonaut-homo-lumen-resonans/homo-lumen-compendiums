
import React, { useState, useRef, useEffect } from 'react';
import { GlobeAltIcon } from '../icons';

const LanguageSwitcher: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('Bokmål');
  const dropdownRef = useRef<HTMLDivElement>(null);

  const languages = {
    available: [
      { code: 'nb', name: 'Bokmål', desc: 'Standard' },
      { code: 'nn', name: 'Nynorsk', desc: 'Påkrevd for offentlige tjenester' },
      { code: 'en', name: 'Engelsk', desc: 'For engelsktalende' },
      { code: 'simple', name: 'Enkel norsk', desc: 'For språksvake' },
    ],
    future: [
      { code: 'ar', name: 'Arabisk', desc: 'Kommer snart' },
      { code: 'so', name: 'Somali', desc: 'Kommer snart' },
      { code: 'ur', name: 'Urdu', desc: 'Kommer snart' },
      { code: 'smi', name: 'Samisk', desc: 'Kommer snart' },
    ]
  };

  const handleLanguageChange = (langName: string) => {
    setSelectedLanguage(langName);
    setIsOpen(false);
    // Here you would typically implement the logic to change the app's language,
    // e.g., using a context or a library like i18next.
    alert(`Språk endret til ${langName} (simulert).`);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);


  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-md hover:bg-lightgray transition-colors"
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        <GlobeAltIcon className="w-6 h-6 text-darkgray" />
        <span className="hidden md:inline text-sm text-darkgray font-medium">{selectedLanguage}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-xl z-50 border">
          <ul className="py-1">
            {languages.available.map(lang => (
              <li key={lang.code}>
                <button
                  onClick={() => handleLanguageChange(lang.name)}
                  className="w-full text-left px-4 py-2 hover:bg-primary-light"
                >
                  <p className="font-medium text-darkgray">{lang.name}</p>
                  <p className="text-xs text-mediumgray">{lang.desc}</p>
                </button>
              </li>
            ))}
             <li className="border-t my-1"></li>
             <li className="px-4 py-2 text-xs text-mediumgray uppercase font-semibold">Fremtidige Språk</li>
            {languages.future.map(lang => (
               <li key={lang.code}>
                <div className="w-full text-left px-4 py-2 opacity-50 cursor-not-allowed">
                  <p className="font-medium text-darkgray">{lang.name}</p>
                  <p className="text-xs text-mediumgray">{lang.desc}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;
