import React, { useState } from 'react';
import { Button } from '@/components/common/Button';
import { Card } from '@/components/common/Card';

export const SettingsPage: React.FC = () => {
  const [confidenceThreshold, setConfidenceThreshold] = useState(80);
  const [failsafeEnabled, setFailsafeEnabled] = useState(true);
  const [cooldown, setCooldown] = useState(1.0);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleSave = () => {
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 2500);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">System Configuration</h2>
        <p className="text-sm text-slate-400 mt-1">
          Tune safety limits, confidence scoring thresholds, and hardware integration parameters.
        </p>
      </div>

      <div className="space-y-6">
        <Card title="Safety and Action Dispatch Guardrails">
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-medium text-slate-200">
                  Global Confidence Threshold ({confidenceThreshold}%)
                </label>
                <span className="text-xs text-slate-400 font-mono">
                  {(confidenceThreshold / 100).toFixed(2)}
                </span>
              </div>
              <input
                type="range"
                min="50"
                max="99"
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                className="w-full accent-brand-500 bg-surface-darkest h-2 rounded-lg cursor-pointer"
              />
              <p className="text-xs text-slate-500 mt-1">
                Gestures classified below this confidence score will never trigger automated desktop actions.
              </p>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-medium text-slate-200">
                  Default Action Cooldown ({cooldown.toFixed(1)} seconds)
                </label>
                <span className="text-xs text-slate-400 font-mono">{cooldown}s</span>
              </div>
              <input
                type="range"
                min="0.2"
                max="5.0"
                step="0.1"
                value={cooldown}
                onChange={(e) => setCooldown(Number(e.target.value))}
                className="w-full accent-brand-500 bg-surface-darkest h-2 rounded-lg cursor-pointer"
              />
              <p className="text-xs text-slate-500 mt-1">
                Minimum cooldown window between repeated automated actions to prevent unintentional repeat triggers.
              </p>
            </div>

            <div className="flex items-center justify-between p-4 rounded-lg bg-surface-darkest/60 border border-surface-border">
              <div>
                <p className="text-sm font-medium text-white">Hardware Fail-Safe Killswitch</p>
                <p className="text-xs text-slate-400 mt-0.5">
                  Immediately aborts cursor simulation if mouse is forcefully moved to any screen corner.
                </p>
              </div>
              <input
                type="checkbox"
                checked={failsafeEnabled}
                onChange={(e) => setFailsafeEnabled(e.target.checked)}
                className="w-4 h-4 accent-brand-500 rounded cursor-pointer"
              />
            </div>
          </div>
        </Card>

        <div className="flex items-center justify-between">
          <div>
            {saveSuccess && (
              <span className="text-xs font-semibold text-emerald-400">
                Settings saved successfully!
              </span>
            )}
          </div>
          <Button onClick={handleSave}>Save Preferences</Button>
        </div>
      </div>
    </div>
  );
};
