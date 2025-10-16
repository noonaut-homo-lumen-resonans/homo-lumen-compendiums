
import React, { useState, useRef, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { APP_NAME, APP_ROUTES } from '../constants';
import { HomeIcon, BookOpenIcon, ChatBubbleLeftEllipsisIcon, DocumentTextIcon, BellIcon, ScaleIcon, CogIcon, LightBulbIcon, HeartIcon, Bars3Icon, BriefcaseIcon } from './icons';

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const navItems = [
    { path: APP_ROUTES.DASHBOARD, label: 'Dashbord', icon: <HomeIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.GUIDES, label: 'Veiledninger', icon: <BookOpenIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.EXPLAIN_LETTER, label: 'Forklar brev', icon: <LightBulbIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.MASTERY, label: 'Mestring', icon: <HeartIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.JOB, label: 'Jobb', icon: <BriefcaseIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.CHATBOT, label: 'Chatbot', icon: <ChatBubbleLeftEllipsisIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.DOCUMENTS, label: 'Dokumenter', icon: <DocumentTextIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.REMINDERS, label: 'Påminnelser', icon: <BellIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.RIGHTS, label: 'Rettigheter', icon: <ScaleIcon className="w-5 h-5" /> },
    { path: APP_ROUTES.SETTINGS, label: 'Innstillinger', icon: <CogIcon className="w-5 h-5" /> },
  ];

  const activeClassName = "bg-primary-dark text-white";
  const inactiveClassName = "text-darkgray hover:bg-primary-light hover:text-primary-dark";

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
        aria-label="Åpne meny"
      >
        <Bars3Icon className="w-6 h-6 text-darkgray" />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-2 w-64 bg-white rounded-lg shadow-xl z-50 border">
          <div className="p-4 border-b">
            <h2 className="text-xl font-bold text-primary">{APP_NAME}</h2>
          </div>
          <nav className="p-2 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) =>
                  `flex items-center space-x-3 p-3 rounded-lg transition-colors duration-200 ${
                    isActive ? activeClassName : inactiveClassName
                  }`
                }
              >
                {item.icon}
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      )}
    </div>
  );
};

export default Sidebar;