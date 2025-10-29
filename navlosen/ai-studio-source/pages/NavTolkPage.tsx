
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AI_DISCLAIMER_SHORT, APP_ROUTES } from '../constants';
import { getExplanationFromGemini } from '../services/geminiService';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { LightBulbIcon, InformationCircleIcon } from '../components/icons';
import { NavTolkState, ExplanationResult } from '../types';

const NavTolkPage: React.FC = () => {
  const [inputText, setInputText] = useState<string>('');
  const [explanation, setExplanation] = useState<ExplanationResult | null>(null);
  const [pageState, setPageState] = useState<NavTolkState>(NavTolkState.IDLE);
  const [error, setError] = useState<string | null>(null);

  const handleExplain = async () => {
    if (!inputText.trim()) {
      setError('Vennligst lim inn tekst som skal forklares.');
      return;
    }
    setPageState(NavTolkState.LOADING);
    setError(null);
    setExplanation(null);

    try {
      const result = await getExplanationFromGemini(inputText);
      if (result) {
        setExplanation(result);
        setPageState(NavTolkState.SUCCESS);
      } else {
         throw new Error("Kunne ikke hente en gyldig forklaring fra tjenesten.");
      }
    } catch (err: any) {
      console.error("Error explaining text:", err);
      setError('Noe gikk galt. Prøv igjen, eller kontakt en veileder via chatten.');
      setPageState(NavTolkState.ERROR);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center mb-4">
          <LightBulbIcon className="w-8 h-8 text-accent mr-3" />
          <h2 className="text-xl font-semibold text-darkgray">Forklar NAV-brev</h2>
        </div>
        <p className="text-mediumgray">
          Lim inn tekst fra et NAV-brev, vedtak, eller en nettside du synes er vanskelig å forstå. 
          Vi hjelper deg med å oversette det til et enklere språk.
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <label htmlFor="nav-text-input" className="block text-sm font-medium text-darkgray mb-2">
            Lim inn tekst fra et NAV-brev. Ikke legg inn fødselsnummer eller kontonummer.
        </label>
        <textarea
          id="nav-text-input"
          rows={8}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-y"
          placeholder="Lim inn teksten her..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          disabled={pageState === NavTolkState.LOADING}
        />
        <div className="mt-4 p-3 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg text-xs">
            <p>{AI_DISCLAIMER_SHORT}</p>
        </div>
        <div className="mt-4 flex flex-col sm:flex-row justify-between items-center gap-4">
          <Button 
            onClick={handleExplain} 
            isLoading={pageState === NavTolkState.LOADING}
            disabled={pageState === NavTolkState.LOADING || !inputText.trim()}
          >
            Forklar dette brevet
          </Button>
          {pageState === NavTolkState.LOADING && <LoadingSpinner text="Forklarer..." />}
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow" role="alert">
          <p className="font-bold">Feil</p>
          <p>{error}</p>
        </div>
      )}

      {pageState === NavTolkState.SUCCESS && explanation && (
        <div className="bg-white p-6 rounded-lg shadow space-y-6">
          <div className="text-center p-3 bg-yellow-50 rounded-md border border-yellow-200">
             <p className="text-sm text-yellow-800">
                Noen NAV-brev kan føles tunge. <Link to={APP_ROUTES.MASTERY} className="font-semibold underline hover:text-yellow-900">Trenger du en liten pause?</Link>
             </p>
          </div>
          <div id="summary-section">
            <h3 className="text-lg font-semibold text-darkgray mb-3">Dette betyr brevet</h3>
            <div className="p-4 bg-lightgray rounded-md whitespace-pre-wrap text-darkgray">
              {explanation.summary}
            </div>
          </div>
          
          <div id="deadlines-section">
            <h3 className="text-lg font-semibold text-darkgray mb-3">Viktige frister</h3>
            <div className="p-4 bg-lightgray rounded-md text-darkgray">
              {explanation.deadlines && explanation.deadlines.length > 0 ? (
                <ul className="list-disc list-inside space-y-2">
                  {explanation.deadlines.map((deadline, index) => (
                    <li key={index}>
                      <strong>{deadline.date}:</strong> {deadline.label}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Ingen spesifikke frister ble funnet i teksten.</p>
              )}
            </div>
          </div>
          
          <div id="next-steps-section">
            <h3 className="text-lg font-semibold text-darkgray mb-3">Hva gjør jeg nå?</h3>
             <div className="p-4 bg-lightgray rounded-md text-darkgray">
              {explanation.nextSteps && explanation.nextSteps.length > 0 ? (
                <ul className="list-disc list-inside space-y-2">
                  {explanation.nextSteps.map((step, index) => (
                    <li key={index}>{step.label}</li>
                  ))}
                </ul>
              ) : (
                <p>Ingen spesifikke neste steg ble identifisert. Les gjennom forklaringen og sjekk nav.no for veiledning.</p>
              )}
            </div>
          </div>
        </div>
      )}
      
       <div className="mt-6 p-4 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg shadow">
        <div className="flex items-start">
          <InformationCircleIcon className="w-6 h-6 mr-2 flex-shrink-0" />
          <div>
            <h4 className="font-semibold">Viktig å huske på:</h4>
            <p className="text-sm">Den forenklede teksten er et hjelpemiddel for forståelse. Det er alltid den originale teksten fra NAV som er juridisk gjeldende.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NavTolkPage;