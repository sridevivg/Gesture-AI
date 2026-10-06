import React from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { Card } from '@/components/common/Card';

const mockConfidenceData = [
  { time: '10:00', confidence: 92 },
  { time: '10:05', confidence: 88 },
  { time: '10:10', confidence: 95 },
  { time: '10:15', confidence: 84 },
  { time: '10:20', confidence: 96 },
  { time: '10:25', confidence: 91 },
  { time: '10:30', confidence: 94 },
];

const mockGestureDistribution = [
  { gesture: 'Pinch', count: 45 },
  { gesture: 'Swipe Right', count: 32 },
  { gesture: 'Swipe Left', count: 28 },
  { gesture: 'Thumbs Up', count: 18 },
  { gesture: 'Open Palm', count: 12 },
];

export const AnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Recognition Analytics</h2>
        <p className="text-sm text-slate-400 mt-1">
          Historical confidence metrics, inference frequency, and telemetry distributions.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Mean Recognition Confidence" subtitle="Average confidence over time (%)">
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockConfidenceData}>
                <defs>
                  <linearGradient id="colorConfidence" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27354f" />
                <XAxis dataKey="time" stroke="#64748b" />
                <YAxis domain={[60, 100]} stroke="#64748b" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#151e32',
                    borderColor: '#27354f',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="confidence"
                  stroke="#818cf8"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorConfidence)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card title="Gesture Trigger Distribution" subtitle="Total verified recognitions by type">
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockGestureDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27354f" />
                <XAxis dataKey="gesture" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#151e32',
                    borderColor: '#27354f',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
};
