import React, { useState, useMemo } from 'react';
import { HeartIcon, InformationCircleIcon } from '../components/icons';
import { MASTERY_FEELINGS, MASTERY_SYMPTOMS, MASTERY_STRATEGIES } from '../constants';
import { MasteryStrategy } from '../types';

const MasteryPage: React.FC = () => {
  const [selectedFeeling, setSelectedFeeling] = useState<string | null>(null);
  const [stressLevel, setStressLevel] = useState<number>(3);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);

  const handleSymptomToggle = (symptom: string) => {
    setSelectedSymptoms(prev => {
      const isSelected = prev.includes(symptom);
      if (isSelected) {
        return prev.filter(s => s !== symptom);
      } else if (prev.length < 3) {
        return [...prev, symptom];
      }
      return prev; // Return previous state if limit is reached
    });
  };

  const recommendedStrategies = useMemo((): MasteryStrategy[] => {
    const highStressSymptoms = ['Rask puls', 'Svimmel / lett i hodet'];
    const hasHighStressSymptom = selectedSymptoms.some(s => highStressSymptoms.includes(s));

    // If no specific input is given, show a varied default list
    const isDefaultState = !selectedFeeling && stressLevel <= 3 && selectedSymptoms.length === 0;
    if (isDefaultState) {
        // Show a broader, more useful set of general strategies by default.
        return MASTERY_STRATEGIES.filter(s => 
            s.tags.includes('all') || s.tags.includes('grounding')
        ).slice(0, 4);
    }
    
    const recommendedSet = new Set<MasteryStrategy>();

    // Add strategies based on high stress
    if (stressLevel >= 4 || hasHighStressSymptom) {
        MASTERY_STRATEGIES.filter(s => s.tags.includes('high-stress') || s.tags.includes('grounding')).forEach(s => recommendedSet.add(s));
    }

    // Add strategies based on feeling
    if (selectedFeeling) {
        const feeling = MASTERY_FEELINGS.find(f => f.label === selectedFeeling);
        if (feeling?.valence === 'unpleasant') {
            MASTERY_STRATEGIES.filter(s => s.tags.includes('calm') || s.tags.includes('grounding')).forEach(s => recommendedSet.add(s));
        }
        if (feeling?.energy === 'low') {
            MASTERY_STRATEGIES.filter(s => s.tags.includes('action') || s.tags.includes('focus')).forEach(s => recommendedSet.add(s));
        }
    }

    // If the set is still small, add some general ones
    if(recommendedSet.size < 3) {
        MASTERY_STRATEGIES.filter(s => s.tags.includes('all')).forEach(s => recommendedSet.add(s));
    }
    
    return Array.from(recommendedSet);

  }, [selectedFeeling, stressLevel, selectedSymptoms]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center mb-4">
          <HeartIcon className="w-8 h-8 text-pink-500 mr-3" />
          <h2 className="text-xl font-semibold text-darkgray">Mestring og Indre Ro</h2>
        </div>
        <p className="text-mediumgray">
          Noen NAV-prosesser kan føles tunge. Her får du en kort pause og små verktøy for å hente ro og fokus. 
          Svarene dine brukes kun til å gi deg relevante forslag her og nå.
        </p>
      </div>

      {/* Input Section */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="space-y-8">
            <div>
                <h3 className="text-lg font-semibold text-darkgray mb-3">Hvordan kjennes det akkurat nå?</h3>
                 <p className="text-sm text-mediumgray mb-3">Velg en følelse som passer best. Dette hjelper oss å foreslå en relevant øvelse.</p>
                <div className="flex flex-wrap gap-2">
                    {MASTERY_FEELINGS.map(feeling => (
                        <button 
                            key={feeling.label}
                            onClick={() => setSelectedFeeling(feeling.label)}
                            className={`px-4 py-2 text-sm font-medium rounded-full border transition-colors ${
                                selectedFeeling === feeling.label 
                                ? 'bg-primary text-white border-primary' 
                                : 'bg-white text-darkgray border-gray-300 hover:bg-lightgray'
                            }`}
                        >
                            {feeling.label}
                        </button>
                    ))}
                </div>
            </div>

            <div>
                 <h3 className="text-lg font-semibold text-darkgray mb-3">Hvor mye trykk kjenner du på?</h3>
                 <div className="flex items-center gap-4">
                    <span className="text-sm text-mediumgray">Lite</span>
                    <input
                        type="range"
                        min="1"
                        max="5"
                        step="1"
                        value={stressLevel}
                        onChange={(e) => setStressLevel(Number(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary"
                        aria-label="Stressnivå-slider"
                    />
                    <span className="text-sm text-mediumgray">Mye</span>
                 </div>
                 <div className="text-center text-darkgray font-semibold mt-2">{stressLevel}</div>
            </div>

            <div>
                <h3 className="text-lg font-semibold text-darkgray mb-3">Kjenner du på noen av disse kroppslige signalene?</h3>
                <p className="text-sm text-mediumgray mb-3">Valgfritt. Velg opptil 3.</p>
                <div className="flex flex-wrap gap-2">
                    {MASTERY_SYMPTOMS.map(symptom => (
                        <button
                            key={symptom}
                            onClick={() => handleSymptomToggle(symptom)}
                            className={`px-4 py-2 text-sm font-medium rounded-full border transition-colors ${
                                selectedSymptoms.includes(symptom)
                                ? 'bg-primary text-white border-primary'
                                : 'bg-white text-darkgray border-gray-300 hover:bg-lightgray'
                            }`}
                        >
                            {symptom}
                        </button>
                    ))}
                </div>
            </div>
        </div>
      </div>
      
      {/* Recommendations Section */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-darkgray mb-4">Anbefalt støtte for deg</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recommendedStrategies.map(strategy => (
            <div key={strategy.id} className="bg-lightgray p-5 rounded-lg border border-gray-200 flex flex-col">
              <h4 className="font-semibold text-darkgray text-md">{strategy.title}</h4>
              <p className="text-sm text-mediumgray mt-1 mb-3 flex-grow">{strategy.description}</p>
              <div className="text-xs font-medium text-primary bg-primary-light w-fit px-2 py-1 rounded-full">{strategy.duration}</div>
            </div>
          ))}
        </div>
      </div>

       <div className="mt-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-800 rounded-lg shadow">
        <div className="flex items-start">
          <InformationCircleIcon className="w-6 h-6 mr-2 flex-shrink-0" />
          <div>
            <h4 className="font-semibold">Viktig ansvarsfraskrivelse:</h4>
            <p className="text-sm">Disse verktøyene er ment for mestringsstøtte og er ikke helsehjelp. De erstatter ikke profesjonell medisinsk eller psykologisk rådgivning. Ved akutt behov for hjelp, kontakt fastlege eller ring 113.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MasteryPage;