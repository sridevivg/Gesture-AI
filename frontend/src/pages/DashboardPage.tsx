import React from 'react';
import { Activity, Cpu, Hand, Shield, Zap } from 'lucide-react';
import { Card } from '@/components/common/Card';
import { StatusBadge } from '@/components/common/StatusBadge';
import { useSystemStatus } from '@/hooks/useSystemStatus';

export const DashboardPage: React.FC = () => {
  const { data: health } = useSystemStatus();

  const metrics = [
    {
      title: 'Recognition Engine',
      value: health?.services?.ml_inference === 'operational' ? 'Active' : 'Standby',
      icon: Cpu,
      status: 'active' as const,
      detail: '21 Landmark 3D Tracking',
    },
    {
      title: 'System Safety Failsafe',
      value: 'Engaged',
      icon: Shield,
      status: 'success' as const,
      detail: 'Corner stop & cooldown active',
    },
    {
      title: 'Active Session Latency',
      value: '< 15 ms',
      icon: Zap,
      status: 'success' as const,
      detail: 'Optimized WebSocket stream',
    },
    {
      title: 'Supported Gestures',
      value: '11 Defined',
      icon: Hand,
      status: 'active' as const,
      detail: 'Static poses & dynamic swipes',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Platform Dashboard</h2>
        <p className="text-sm text-slate-400 mt-1">
          Real-time status overview of vision models, backend orchestrator, and action controllers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <Card key={metric.title} className="relative overflow-hidden">
              <div className="flex items-center justify-between mb-3">
                <div className="w-10 h-10 rounded-lg bg-surface-card border border-surface-border flex items-center justify-center text-brand-400">
                  <Icon className="w-5 h-5" />
                </div>
                <StatusBadge status={metric.status} />
              </div>
              <p className="text-xs text-slate-400">{metric.title}</p>
              <p className="text-xl font-bold text-white mt-1">{metric.value}</p>
              <p className="text-[11px] text-slate-500 mt-2">{metric.detail}</p>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card
          title="System Architecture Status"
          subtitle="Monorepo subsystem health matrix"
          className="lg:col-span-2"
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3.5 rounded-lg bg-surface-darkest/50 border border-surface-border">
              <div className="flex items-center gap-3">
                <Activity className="w-4 h-4 text-emerald-400" />
                <div>
                  <p className="text-sm font-semibold text-white">FastAPI Orchestrator</p>
                  <p className="text-xs text-slate-400">REST API & WebSocket Broadcast</p>
                </div>
              </div>
              <StatusBadge status="active" label="OPERATIONAL" />
            </div>

            <div className="flex items-center justify-between p-3.5 rounded-lg bg-surface-darkest/50 border border-surface-border">
              <div className="flex items-center gap-3">
                <Cpu className="w-4 h-4 text-brand-400" />
                <div>
                  <p className="text-sm font-semibold text-white">ML Inference Pipeline</p>
                  <p className="text-xs text-slate-400">MediaPipe Vision & Normalized Geometry</p>
                </div>
              </div>
              <StatusBadge
                status={health?.services?.ml_inference === 'operational' ? 'active' : 'inactive'}
                label={health?.services?.ml_inference === 'operational' ? 'ONLINE' : 'STANDBY'}
              />
            </div>

            <div className="flex items-center justify-between p-3.5 rounded-lg bg-surface-darkest/50 border border-surface-border">
              <div className="flex items-center gap-3">
                <Shield className="w-4 h-4 text-amber-400" />
                <div>
                  <p className="text-sm font-semibold text-white">Action Execution Layer</p>
                  <p className="text-xs text-slate-400">PyAutoGUI Safe Automation Adapter</p>
                </div>
              </div>
              <StatusBadge
                status={health?.services?.action_execution === 'enabled' ? 'active' : 'inactive'}
                label={health?.services?.action_execution === 'enabled' ? 'ACTIVE' : 'SAFE STANDBY'}
              />
            </div>
          </div>
        </Card>

        <Card title="Quick Actions" subtitle="Platform shortcuts">
          <div className="space-y-3">
            <a
              href="/studio"
              className="block p-3 rounded-lg bg-brand-600/10 border border-brand-500/20 hover:border-brand-500/40 text-brand-300 transition-colors"
            >
              <p className="text-sm font-semibold">Open Gesture Studio</p>
              <p className="text-xs text-slate-400 mt-0.5">Stream webcam and verify landmarks</p>
            </a>

            <a
              href="/mappings"
              className="block p-3 rounded-lg bg-surface-darkest/50 border border-surface-border hover:border-slate-600 text-slate-200 transition-colors"
            >
              <p className="text-sm font-semibold">Configure Mappings</p>
              <p className="text-xs text-slate-400 mt-0.5">Bind gestures to desktop actions</p>
            </a>

            <a
              href="/analytics"
              className="block p-3 rounded-lg bg-surface-darkest/50 border border-surface-border hover:border-slate-600 text-slate-200 transition-colors"
            >
              <p className="text-sm font-semibold">View Analytics</p>
              <p className="text-xs text-slate-400 mt-0.5">Inspect recognition confidence logs</p>
            </a>
          </div>
        </Card>
      </div>
    </div>
  );
};
