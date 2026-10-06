import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Header } from '@/components/common/Header';
import { Sidebar } from '@/components/common/Sidebar';
import { ActionMappingsPage } from '@/pages/ActionMappingsPage';
import { AnalyticsPage } from '@/pages/AnalyticsPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { GestureStudioPage } from '@/pages/GestureStudioPage';
import { SettingsPage } from '@/pages/SettingsPage';

export const AppRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen w-screen overflow-hidden bg-surface-darkest text-slate-100">
        <Sidebar />
        <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto p-6 lg:p-8">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/studio" element={<GestureStudioPage />} />
              <Route path="/mappings" element={<ActionMappingsPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
};
