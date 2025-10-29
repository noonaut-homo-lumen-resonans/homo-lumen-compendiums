import React from 'react';
import { Link } from 'react-router-dom';
import { APP_ROUTES, MOCK_NAV_CASES, MOCK_REMINDERS, MOCK_JOB_APPLICATIONS } from '../constants';
import { BookOpenIcon, LightBulbIcon, ChatBubbleLeftEllipsisIcon, DocumentTextIcon, BellIcon, BriefcaseIcon, ChevronRightIcon } from '../components/icons';
import Button from '../components/common/Button';

const DashboardPage: React.FC = () => {
  const quickLinks = [
    { to: APP_ROUTES.GUIDES, label: 'Finn Veiledning', icon: <BookOpenIcon className="w-8 h-8 text-primary" /> },
    { to: APP_ROUTES.EXPLAIN_LETTER, label: 'Forklar NAV-brev', icon: <LightBulbIcon className="w-8 h-8 text-primary" /> },
    { to: APP_ROUTES.CHATBOT, label: 'Spør Chatbot', icon: <ChatBubbleLeftEllipsisIcon className="w-8 h-8 text-primary" /> },
    { to: APP_ROUTES.JOB, label: 'Søk Jobb', icon: <BriefcaseIcon className="w-8 h-8 text-primary" /> },
    { to: APP_ROUTES.DOCUMENTS, label: 'Mine Dokumenter', icon: <DocumentTextIcon className="w-8 h-8 text-primary" /> },
  ];

  const upcomingReminders = MOCK_REMINDERS.filter(r => !r.completed).slice(0, 3);
  const activeCases = MOCK_NAV_CASES.slice(0, 2); // Adjusted to fit 3-col layout better
  const recentApplications = MOCK_JOB_APPLICATIONS.slice(0, 2);
  
  const caseStatusColors: { [key: string]: string } = {
    'Under behandling': 'bg-blue-100 text-blue-800',
    'Mottatt': 'bg-green-100 text-green-800',
    'Trenger oppfølging': 'bg-yellow-100 text-yellow-800',
  };

  const applicationStatusColors: { [key: string]: string } = {
    'Søknad sendt': 'bg-blue-100 text-blue-800',
    'Under vurdering': 'bg-yellow-100 text-yellow-800',
    'Intervju': 'bg-green-100 text-green-800',
    'Avslag': 'bg-red-100 text-red-800',
  };


  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
            <div>
              <h2 className="text-xl font-semibold text-darkgray mb-2">Velkommen til NAV-Losen!</h2>
              <p className="text-mediumgray">Her får du hjelp til å navigere i NAV-systemet. Start med en av snarveiene under, eller se dine aktive saker og påminnelser.</p>
            </div>
            <Link to={APP_ROUTES.CHATBOT} className="mt-4 sm:mt-0">
                <Button variant="outline">Kontakt veileder</Button>
            </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {quickLinks.map(link => (
          <Link key={link.to} to={link.to} className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow flex flex-col items-center justify-center text-center">
            {link.icon}
            <span className="mt-2 font-medium text-darkgray">{link.label}</span>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-darkgray mb-3 flex items-center">
            <BellIcon className="w-6 h-6 text-accent mr-2" />
            Kommende Påminnelser
          </h3>
          {upcomingReminders.length > 0 ? (
            <ul className="space-y-2">
              {upcomingReminders.map(reminder => (
                <li key={reminder.id} className="p-3 bg-lightgray rounded">
                  <p className="font-medium text-darkgray">{reminder.title}</p>
                  <p className="text-sm text-mediumgray">Frist: {reminder.dueDate}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-mediumgray">Ingen kommende påminnelser.</p>
          )}
           <Link to={APP_ROUTES.REMINDERS} className="mt-4 inline-block text-primary hover:underline">Se alle påminnelser</Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-darkgray mb-3">Aktive Saker (Eksempel)</h3>
           {activeCases.length > 0 ? (
            <ul className="space-y-3">
              {activeCases.map(navCase => (
                <li key={navCase.id} className="p-3 bg-lightgray rounded">
                  <div className="flex justify-between items-center mb-1">
                    <p className="font-medium text-darkgray">{navCase.title}</p>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${caseStatusColors[navCase.status] || 'bg-gray-100 text-gray-800'}`}>
                      {navCase.status}
                    </span>
                  </div>
                  <p className="text-sm text-mediumgray">Neste steg: {navCase.nextStep}</p>
                  <p className="text-xs text-gray-400 mt-1">Oppdatert: {navCase.lastUpdated}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-mediumgray">Ingen aktive saker registrert (dette er mock data).</p>
          )}
          <p className="text-xs text-mediumgray mt-3">Merk: Faktisk saksstatus hentes fra NAV. Denne funksjonen er under utvikling.</p>
        </div>
        
        {/* New Job Search Teaser Card */}
        <div className="bg-white p-6 rounded-lg shadow opacity-75">
            <h3 className="text-lg font-semibold text-darkgray mb-3 flex items-center">
                <BriefcaseIcon className="w-6 h-6 text-accent mr-2" />
                Min Jobbsøking <span className="text-sm font-normal ml-2">(Fremtidsvisjon)</span>
            </h3>
            {recentApplications.length > 0 ? (
            <ul className="space-y-3">
                {recentApplications.map(app => (
                <li key={app.id} className="p-3 bg-lightgray rounded">
                    <div className="flex justify-between items-center">
                    <p className="font-medium text-darkgray truncate">{app.jobTitle}</p>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full whitespace-nowrap ${applicationStatusColors[app.status] || 'bg-gray-100 text-gray-800'}`}>
                        {app.status}
                    </span>
                    </div>
                    <p className="text-sm text-mediumgray">{app.company}</p>
                </li>
                ))}
            </ul>
            ) : (
            <p className="text-mediumgray">Ingen nylige søknader.</p>
            )}
            <Link to={APP_ROUTES.JOB} className="mt-4 inline-flex items-center text-primary hover:underline">
                Se jobbside <ChevronRightIcon className="w-4 h-4 ml-1" />
            </Link>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;