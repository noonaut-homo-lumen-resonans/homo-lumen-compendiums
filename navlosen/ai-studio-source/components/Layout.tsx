
import React from 'react';
import { Link } from 'react-router-dom';
import Header from './Header';
import { GENERAL_DISCLAIMER, APP_ROUTES } from '../constants';
import { ChatBubbleLeftEllipsisIcon } from './icons';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-lightgray">
      <Header />
      <main className="flex-1 overflow-y-auto p-6">
        {children}
         <footer className="mt-8 p-4 bg-white rounded-lg shadow text-center text-sm text-gray-600">
          <p>{GENERAL_DISCLAIMER}</p>
        </footer>
      </main>

      {/* Sticky Floating Action Button */}
      <Link
        to={APP_ROUTES.CHATBOT}
        className="fixed bottom-6 right-6 bg-secondary hover:bg-secondary-dark text-white font-semibold py-3 px-4 rounded-full shadow-lg flex items-center space-x-2 transition-transform transform hover:scale-105"
        aria-label="Snakk med en veileder"
      >
        <ChatBubbleLeftEllipsisIcon className="w-6 h-6" />
        <span className="hidden sm:inline">Snakk med veileder</span>
      </Link>
    </div>
  );
};

export default Layout;