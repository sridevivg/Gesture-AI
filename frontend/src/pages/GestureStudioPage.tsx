import React from 'react';
import { CameraFeedPlaceholder } from '@/components/camera/CameraFeedPlaceholder';
import { Card } from '@/components/common/Card';
import { StatusBadge } from '@/components/common/StatusBadge';
import { useGestureStream } from '@/hooks/useGestureStream';

export const GestureStudioPage: React.FC = () => {
  const { isConnected, latestEvent, history } = useGestureStream();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Gesture Studio</h2>
          <p className="text-sm text-slate-400 mt-1">
            Real-time camera feed testing, hand landmark tracking, and intent prediction.
          </p>
        </div>
        <StatusBadge
          status={isConnected ? 'active' : 'inactive'}
          label={isConnected ? 'STREAM CONNECTED' : 'STREAM DISCONNECTED'}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <CameraFeedPlaceholder
            detectedGesture={latestEvent?.gesture || 'None'}
            confidence={latestEvent?.confidence || 0}
            streaming={isConnected}
          />
        </div>

        <div className="space-y-6">
          <Card title="Recognition Telemetry" subtitle="Active inference results">
            <div className="space-y-4">
              <div>
                <span className="text-xs text-slate-400">Classified Gesture</span>
                <p className="text-lg font-bold text-white font-mono mt-0.5">
                  {latestEvent?.gesture || 'Waiting for frame...'}
                </p>
              </div>

              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Confidence Score</span>
                  <span className="font-mono text-brand-400">
                    {latestEvent?.confidence ? `${(latestEvent.confidence * 100).toFixed(1)}%` : '0.0%'}
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-surface-darkest overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-brand-600 to-indigo-400 transition-all duration-200"
                    style={{ width: `${(latestEvent?.confidence || 0) * 100}%` }}
                  />
                </div>
              </div>

              <div className="pt-2 border-t border-surface-border">
                <span className="text-xs text-slate-400">Action Execution</span>
                <p className="text-sm text-slate-200 mt-1">
                  {latestEvent?.action?.executed ? (
                    <span className="text-emerald-400 font-medium">
                      Triggered {latestEvent.action.action_type}
                    </span>
                  ) : (
                    <span className="text-slate-500">Standby (No Action Fired)</span>
                  )}
                </p>
              </div>
            </div>
          </Card>

          <Card title="Recent Event Stream" subtitle="Last detected gestures">
            {history.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">
                No gestures recorded yet. Start camera feed to begin.
              </p>
            ) : (
              <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                {history.slice(0, 10).map((event, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-2 rounded bg-surface-darkest/60 border border-surface-border text-xs"
                  >
                    <span className="font-mono font-medium text-slate-200">{event.gesture}</span>
                    <span className="font-mono text-brand-400">
                      {(event.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
