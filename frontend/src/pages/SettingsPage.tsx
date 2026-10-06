import React, { useState } from 'react';
import { Button } from '@/components/common/Button';
import { Card } from '@/components/common/Card';

export const SettingsPage: React.FC = () => {
  const [confidenceThreshold, setConfidenceThreshold] = useState(80);
  const [failsafeEnabled, setFailsafeEnabled] = useState(true);
  const [cooldown, setCooldown] = useState(1.0);
  const [controlMode, setControlMode] = useState('Presentation');
  const [cameraResolution, setCameraResolution] = useState('640x480');
  const [targetFps, setTargetFps] = useState(30);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const [enabledGestures, setEnabledGestures] = useState<Record<string, boolean>>({
    PINCH: true,
    SWIPE_RIGHT: true,
    SWIPE_LEFT: true,
    THUMBS_UP: true,
    THUMBS_DOWN: true,
    OPEN_PALM: false,
  });

  const toggleGesture = (gesture: string) => {
    setEnabledGestures((prev) => ({
      ...prev,
      [gesture]: !prev[gesture],
    }));
  };

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
        {/* Control Mode Selection */}
        <Card title="Active Control Mode">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {['Presentation', 'Media', 'Desktop', 'Disabled'].map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setControlMode(mode)}
                className={`py-3 px-4 rounded-xl border text-sm font-semibold transition-all ${
                  controlMode === mode
                    ? 'bg-brand-500/20 border-brand-500 text-brand-400 shadow-md'
                    : 'bg-surface-darkest/60 border-surface-border text-slate-400 hover:text-white'
                }`}
              >
                {mode}
              </button>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-3">
            Sets the primary context for dispatched gesture commands and shortcuts.
          </p>
        </Card>

        {/* Safety and Action Dispatch */}
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

        {/* Enabled Gestures Preferences */}
        <Card title="Gesture Activation Preferences">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {Object.entries(enabledGestures).map(([gesture, enabled]) => (
              <label
                key={gesture}
                className="flex items-center justify-between p-3 rounded-lg bg-surface-darkest/50 border border-surface-border cursor-pointer hover:border-surface-border/80"
              >
                <span className="text-sm font-mono text-slate-300">{gesture}</span>
                <input
                  type="checkbox"
                  checked={enabled}
                  onChange={() => toggleGesture(gesture)}
                  className="w-4 h-4 accent-brand-500 rounded cursor-pointer"
                />
              </label>
            ))}
          </div>
        </Card>

        {/* Camera Hardware Preferences */}
        <Card title="Vision & Camera Hardware Settings">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Capture Resolution</label>
              <select
                value={cameraResolution}
                onChange={(e) => setCameraResolution(e.target.value)}
                className="w-full px-3 py-2 bg-surface-darkest border border-surface-border rounded-lg text-sm text-white"
              >
                <option value="640x480">640 x 480 (Recommended)</option>
                <option value="1280x720">1280 x 720 (HD)</option>
                <option value="320x240">320 x 240 (Low Latency)</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Target Detection Rate</label>
              <select
                value={targetFps}
                onChange={(e) => setTargetFps(Number(e.target.value))}
                className="w-full px-3 py-2 bg-surface-darkest border border-surface-border rounded-lg text-sm text-white"
              >
                <option value={30}>30 FPS (Smooth)</option>
                <option value={60}>60 FPS (Ultra-responsive)</option>
                <option value={15}>15 FPS (Battery Saver)</option>
              </select>
            </div>
          </div>
        </Card>

        <div className="flex items-center justify-between pt-2">
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
