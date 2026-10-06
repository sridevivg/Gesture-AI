import React, { useRef, useState } from 'react';
import { Camera, CameraOff, Video } from 'lucide-react';
import { Button } from '@/components/common/Button';

interface CameraFeedPlaceholderProps {
  detectedGesture?: string;
  confidence?: number;
  streaming?: boolean;
}

export const CameraFeedPlaceholder: React.FC<CameraFeedPlaceholderProps> = ({
  detectedGesture = 'None',
  confidence = 0,
  streaming = false,
}) => {
  const [cameraActive, setCameraActive] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const toggleCamera = async () => {
    if (cameraActive) {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach((track) => track.stop());
        videoRef.current.srcObject = null;
      }
      setCameraActive(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 },
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        setCameraActive(true);
      } catch (err) {
        console.warn('WebCam access error:', err);
      }
    }
  };

  return (
    <div className="relative rounded-2xl overflow-hidden bg-surface-darkest border border-surface-border aspect-video flex flex-col items-center justify-center group shadow-2xl">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className={`absolute inset-0 w-full h-full object-cover -scale-x-100 ${
          cameraActive ? 'opacity-100' : 'opacity-0'
        }`}
      />

      {/* Grid overlay for computer vision aesthetic */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f293d15_1px,transparent_1px),linear-gradient(to_bottom,#1f293d15_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />

      {!cameraActive && (
        <div className="z-10 flex flex-col items-center gap-3 text-slate-500">
          <div className="w-16 h-16 rounded-full bg-surface-card/80 border border-surface-border flex items-center justify-center text-slate-400">
            <Video className="w-8 h-8" />
          </div>
          <p className="text-sm font-medium text-slate-300">Camera Feed Inactive</p>
          <p className="text-xs text-slate-500 max-w-xs text-center">
            Enable client video to capture hand landmarks and stream to the recognition engine.
          </p>
        </div>
      )}

      {/* HUD Telemetry Overlay */}
      <div className="absolute top-4 left-4 z-20 flex items-center gap-2">
        <span
          className={`flex h-2.5 w-2.5 rounded-full ${
            streaming ? 'bg-emerald-500 animate-ping' : 'bg-slate-600'
          }`}
        />
        <span className="text-xs font-mono font-medium px-2 py-1 rounded bg-black/60 backdrop-blur text-slate-300 border border-white/10">
          STREAM: {streaming ? 'CONNECTED' : 'DISCONNECTED'}
        </span>
      </div>

      <div className="absolute top-4 right-4 z-20">
        <Button
          size="sm"
          variant={cameraActive ? 'secondary' : 'primary'}
          onClick={toggleCamera}
          className="gap-2 shadow-lg"
        >
          {cameraActive ? (
            <>
              <CameraOff className="w-4 h-4" /> Stop Camera
            </>
          ) : (
            <>
              <Camera className="w-4 h-4" /> Start Camera
            </>
          )}
        </Button>
      </div>

      {/* Gesture Recognition Banner */}
      <div className="absolute bottom-4 inset-x-4 z-20 flex items-center justify-between px-4 py-3 rounded-xl bg-black/70 backdrop-blur border border-white/10">
        <div>
          <span className="text-[11px] text-slate-400 uppercase tracking-wider block">
            Current Gesture
          </span>
          <span className="text-sm font-bold text-white tracking-wide">
            {detectedGesture}
          </span>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 uppercase tracking-wider block">
            Confidence
          </span>
          <span className="text-sm font-mono font-semibold text-brand-400">
            {(confidence * 100).toFixed(0)}%
          </span>
        </div>
      </div>
    </div>
  );
};
