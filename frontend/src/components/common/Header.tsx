import React from 'react';
import { Activity, Radio, ShieldCheck } from 'lucide-react';
import { useSystemStatus } from '@/hooks/useSystemStatus';

export const Header: React.FC = () => {
  const { data: health, isLoading } = useSystemStatus();

  return (
    <header className="h-16 border-b border-surface-border bg-surface-darker/60 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-white tracking-wide flex items-center gap-2">
            Gesture-AI <span className="text-xs px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20">Studio</span>
          </h1>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-surface-card border border-surface-border text-xs">
          <Radio className={`w-3.5 h-3.5 ${isLoading ? 'text-amber-400' : 'text-emerald-400 animate-pulse'}`} />
          <span className="text-slate-400">Backend:</span>
          <span className="font-semibold text-slate-200">
            {isLoading ? 'Connecting...' : health?.status === 'healthy' ? 'Online' : 'Offline'}
          </span>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-surface-card border border-surface-border text-xs">
          <ShieldCheck className="w-3.5 h-3.5 text-brand-400" />
          <span className="text-slate-400">Actions:</span>
          <span className="font-semibold text-slate-200">
            {health?.services?.action_execution === 'enabled' ? 'Active' : 'Safe Standby'}
          </span>
        </div>
      </div>
    </header>
  );
};
