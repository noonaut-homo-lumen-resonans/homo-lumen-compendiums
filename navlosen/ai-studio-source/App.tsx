
import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import GuidesPage from './pages/GuidesPage';
import GuideDetailPage from './pages/GuideDetailPage';
import NavTolkPage from './pages/NavTolkPage';
import ChatbotPage from './pages/ChatbotPage';
import DocumentsPage from './pages/DocumentsPage';
import RemindersPage from './pages/RemindersPage';
import RightsPage from './pages/RightsPage';
import SettingsPage from './pages/SettingsPage';
import MasteryPage from './pages/MasteryPage';
import JobPage from './pages/JobPage'; // Import the new page
import { APP_ROUTES } from './constants';

const App: React.FC = () => {
  return (
    <HashRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to={APP_ROUTES.DASHBOARD} replace />} />
          <Route path={APP_ROUTES.DASHBOARD} element={<DashboardPage />} />
          <Route path={APP_ROUTES.GUIDES} element={<GuidesPage />} />
          <Route path={`${APP_ROUTES.GUIDES}/:id`} element={<GuideDetailPage />} />
          <Route path={APP_ROUTES.EXPLAIN_LETTER} element={<NavTolkPage />} />
          <Route path={APP_ROUTES.CHATBOT} element={<ChatbotPage />} />
          <Route path={APP_ROUTES.DOCUMENTS} element={<DocumentsPage />} />
          <Route path={APP_ROUTES.REMINDERS} element={<RemindersPage />} />
          <Route path={APP_ROUTES.RIGHTS} element={<RightsPage />} />
          <Route path={APP_ROUTES.SETTINGS} element={<SettingsPage />} />
          <Route path={APP_ROUTES.MASTERY} element={<MasteryPage />} />
          <Route path={APP_ROUTES.JOB} element={<JobPage />} /> {/* Add the new route */}
        </Routes>
      </Layout>
    </HashRouter>
  );
};

export default App;