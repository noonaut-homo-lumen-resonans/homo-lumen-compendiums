
import React, { useState } from 'react';
import Button from '../components/common/Button';
import { CogIcon, UserCircleIcon, BellIcon, LockClosedIcon } from '../components/icons';

const SettingsPage: React.FC = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [emailForSummary, setEmailForSummary] = useState(false);
  const [fontSize, setFontSize] = useState('normal'); // 'normal', 'large', 'extra-large'

  const handleSaveChanges = () => {
    // In a real app, this would save to a backend or local storage
    alert('Innstillinger lagret (simulert)!');
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center mb-4">
          <CogIcon className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-xl font-semibold text-darkgray">Innstillinger</h2>
        </div>
        <p className="text-mediumgray">
          Administrer dine preferanser for NAV-Losen applikasjonen.
        </p>
      </div>

      {/* Profilinnstillinger (Mock) */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-darkgray mb-4 flex items-center">
          <UserCircleIcon className="w-6 h-6 text-gray-500 mr-2" />
          Profilinnstillinger (Eksempel)
        </h3>
        <div className="space-y-4">
          <div>
            <label htmlFor="userName" className="block text-sm font-medium text-darkgray">Brukernavn (display)</label>
            <input type="text" id="userName" defaultValue="Bruker Mock" className="mt-1 block w-full md:w-1/2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm" />
          </div>
          <div>
            <label htmlFor="userEmail" className="block text-sm font-medium text-darkgray">E-post (for varsler)</label>
            <input type="email" id="userEmail" defaultValue="bruker@example.com" className="mt-1 block w-full md:w-1/2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm" />
          </div>
        </div>
      </div>

      {/* Varslingsinnstillinger */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-darkgray mb-4 flex items-center">
          <BellIcon className="w-6 h-6 text-gray-500 mr-2" />
          Varslingsinnstillinger
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-mediumgray">Aktiver push-varsler for påminnelser</span>
            <label htmlFor="toggleNotifications" className="flex items-center cursor-pointer">
              <div className="relative">
                <input type="checkbox" id="toggleNotifications" className="sr-only" checked={notificationsEnabled} onChange={() => setNotificationsEnabled(!notificationsEnabled)} />
                <div className={`block w-14 h-8 rounded-full ${notificationsEnabled ? 'bg-primary' : 'bg-gray-300'}`}></div>
                <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform ${notificationsEnabled ? 'transform translate-x-6' : ''}`}></div>
              </div>
            </label>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-mediumgray">Motta ukentlig sammendrag på e-post</span>
             <label htmlFor="toggleEmailSummary" className="flex items-center cursor-pointer">
              <div className="relative">
                <input type="checkbox" id="toggleEmailSummary" className="sr-only" checked={emailForSummary} onChange={() => setEmailForSummary(!emailForSummary)} />
                <div className={`block w-14 h-8 rounded-full ${emailForSummary ? 'bg-primary' : 'bg-gray-300'}`}></div>
                <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform ${emailForSummary ? 'transform translate-x-6' : ''}`}></div>
              </div>
            </label>
          </div>
        </div>
      </div>
      
      {/* Tilgjengelighetsinnstillinger */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-darkgray mb-4">Tilgjengelighet</h3>
        <div>
          <label htmlFor="fontSize" className="block text-sm font-medium text-darkgray">Tekststørrelse</label>
          <select 
            id="fontSize" 
            value={fontSize} 
            onChange={(e) => setFontSize(e.target.value)}
            className="mt-1 block w-full md:w-1/2 px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
          >
            <option value="normal">Normal</option>
            <option value="large">Stor</option>
            <option value="extra-large">Ekstra Stor</option>
          </select>
          {/* Implement actual font size change in a real app via context or CSS variables */}
           <p className="text-xs text-mediumgray mt-1">Endring av tekststørrelse vil påvirke hele applikasjonen (simulert).</p>
        </div>
      </div>


      {/* Data & Personvern (Kognitiv Suverenitet) */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-darkgray mb-4 flex items-center">
           <LockClosedIcon className="w-6 h-6 text-gray-500 mr-2" />
           Data og Personvern
        </h3>
        <p className="text-mediumgray mb-4">
          NAV-Losen er designet med ditt personvern i fokus. Her kan du (i en fullverdig versjon) administrere dine data.
        </p>
        <div className="space-y-3 sm:space-y-0 sm:space-x-3 flex flex-col sm:flex-row items-start">
          <Button variant="secondary" onClick={() => alert('Funksjon for å laste ned dine data (simulert).')}>Last ned mine data</Button>
          <Button variant="danger" onClick={() => alert('Funksjon for å slette all din data og konto (simulert). Vær forsiktig!')}>Slett min konto og data</Button>
        </div>
         <p className="text-xs text-mediumgray mt-4">Disse funksjonene er eksempler på hvordan NAV-Losen vil støtte din rett til datakontroll ("kognitiv suverenitet"). I en ekte app vil dette være koblet til robuste backend-systemer og følge GDPR-retningslinjer.</p>
      </div>

      <div className="mt-8 flex justify-end">
        <Button onClick={handleSaveChanges} size="lg">
          Lagre Innstillinger
        </Button>
      </div>
    </div>
  );
};

export default SettingsPage;