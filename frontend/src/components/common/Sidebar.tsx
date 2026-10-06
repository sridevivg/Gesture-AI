import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Camera,
  Sliders,
  BarChart3,
  Settings,
} from 'lucide-react';

const navigationItems = [
  { name: 'Dashboard', to: '/', icon: LayoutDashboard },
  { name: 'Gesture Studio', to: '/studio', icon: Camera },
  { name: 'Action Mappings', to: '/mappings', icon: Sliders },
  { name: 'Analytics', to: '/analytics', icon: BarChart3 },
  { name: 'Settings', to: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 border-r border-surface-border bg-surface-darker/50 flex flex-col justify-between p-4">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold tracking-wider text-slate-400 uppercase">
          Navigation
        </div>
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-brand-600 text-white shadow-md shadow-brand-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-surface-card/60'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </div>

      <div className="p-3 rounded-lg bg-surface-card border border-surface-border text-xs text-slate-400 space-y-1">
        <p className="font-semibold text-slate-300">Gesture-AI Engine</p>
        <p className="text-[11px] text-slate-500">v0.1.0 • Core Architecture</p>
      </div>
    </aside>
  );
};
