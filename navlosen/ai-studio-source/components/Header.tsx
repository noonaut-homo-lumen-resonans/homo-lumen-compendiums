
import React from 'react';
import { useLocation } from 'react-router-dom';
import { APP_ROUTES, APP_NAME } from '../constants';
import { UserCircleIcon } from './icons';
import LanguageSwitcher from './common/LanguageSwitcher';
import Sidebar from './Sidebar';

const Header: React.FC = () => {
  const location = useLocation();

  const getPageTitle = () => {
    switch (location.pathname.split('/')[1]) { // Get base path
      case APP_ROUTES.DASHBOARD.split('/')[1]: return 'Dashbord';
      case APP_ROUTES.GUIDES.split('/')[1]: return 'Veiledninger';
      case APP_ROUTES.EXPLAIN_LETTER.split('/')[1]: return 'Forklar brev';
      case APP_ROUTES.CHATBOT.split('/')[1]: return 'Chatbot';
      case APP_ROUTES.DOCUMENTS.split('/')[1]: return 'Mine Dokumenter';
      case APP_ROUTES.REMINDERS.split('/')[1]: return 'Påminnelser';
      case APP_ROUTES.RIGHTS.split('/')[1]: return 'Dine Rettigheter';
      case APP_ROUTES.SETTINGS.split('/')[1]: return 'Innstillinger';
      case APP_ROUTES.MASTERY.split('/')[1]: return 'Mestring';
      case APP_ROUTES.JOB.split('/')[1]: return 'Jobbsøk';
      default: return APP_NAME;
    }
  };

  return (
    <header className="h-20 bg-white shadow-md flex items-center justify-between px-6 flex-shrink-0">
      <div className="flex items-center space-x-4">
        <Sidebar />
        <h1 className="text-xl sm:text-2xl font-semibold text-darkgray">{getPageTitle()}</h1>
      </div>
      <div className="flex items-center space-x-4">
        <LanguageSwitcher />
        <div className="flex items-center space-x-2">
            <span className="hidden sm:inline text-darkgray">Velkommen, Bruker (Mock)</span>
            <UserCircleIcon className="w-8 h-8 text-primary" />
        </div>
      </div>
    </header>
  );
};

export default Header;