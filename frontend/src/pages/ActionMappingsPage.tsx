import React, { useState } from 'react';
import { Sliders, ToggleLeft, ToggleRight } from 'lucide-react';
import { Card } from '@/components/common/Card';
import { StatusBadge } from '@/components/common/StatusBadge';

interface MappingItem {
  id: string;
  gesture: string;
  category: 'static' | 'dynamic';
  action: string;
  cooldown: number;
  enabled: boolean;
}

const initialMappings: MappingItem[] = [
  { id: '1', gesture: 'PINCH', category: 'static', action: 'Primary Mouse Click', cooldown: 0.8, enabled: true },
  { id: '2', gesture: 'SWIPE_RIGHT', category: 'dynamic', action: 'Presentation Next Slide', cooldown: 1.2, enabled: true },
  { id: '3', gesture: 'SWIPE_LEFT', category: 'dynamic', action: 'Presentation Previous Slide', cooldown: 1.2, enabled: true },
  { id: '4', gesture: 'THUMBS_UP', category: 'static', action: 'Volume Up (+5%)', cooldown: 0.5, enabled: true },
  { id: '5', gesture: 'THUMBS_DOWN', category: 'static', action: 'Volume Down (-5%)', cooldown: 0.5, enabled: true },
  { id: '6', gesture: 'OPEN_PALM', category: 'static', action: 'Media Play / Pause Toggle', cooldown: 1.5, enabled: false },
];

export const ActionMappingsPage: React.FC = () => {
  const [mappings, setMappings] = useState<MappingItem[]>(initialMappings);

  const toggleMapping = (id: string) => {
    setMappings((prev) =>
      prev.map((item) => (item.id === id ? { ...item, enabled: !item.enabled } : item))
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Action Mappings</h2>
        <p className="text-sm text-slate-400 mt-1">
          Configure how recognized hand gestures trigger safe host computer actions.
        </p>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-surface-border text-xs uppercase tracking-wider text-slate-400 bg-surface-darkest/40">
              <tr>
                <th className="py-3 px-4">Gesture</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Target Action</th>
                <th className="py-3 px-4">Cooldown</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4 text-right">Toggle</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {mappings.map((item) => (
                <tr key={item.id} className="hover:bg-surface-card/40 transition-colors">
                  <td className="py-3 px-4 font-mono font-bold text-white flex items-center gap-2">
                    <Sliders className="w-4 h-4 text-brand-400" />
                    {item.gesture}
                  </td>
                  <td className="py-3 px-4">
                    <span className="text-xs px-2 py-0.5 rounded bg-surface-darker text-slate-300 border border-surface-border">
                      {item.category}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-200">{item.action}</td>
                  <td className="py-3 px-4 font-mono text-slate-400 text-xs">{item.cooldown}s</td>
                  <td className="py-3 px-4">
                    <StatusBadge
                      status={item.enabled ? 'active' : 'inactive'}
                      label={item.enabled ? 'ENABLED' : 'DISABLED'}
                    />
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button
                      onClick={() => toggleMapping(item.id)}
                      className="text-slate-400 hover:text-white transition-colors"
                      title="Toggle action state"
                    >
                      {item.enabled ? (
                        <ToggleRight className="w-6 h-6 text-brand-400" />
                      ) : (
                        <ToggleLeft className="w-6 h-6 text-slate-600" />
                      )}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
