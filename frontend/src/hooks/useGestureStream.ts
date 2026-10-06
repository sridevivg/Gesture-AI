import { useEffect, useRef, useState } from 'react';
import { GestureStreamClient } from '@/services/websocket';
import { GestureStreamEvent } from '@/types';

export function useGestureStream() {
  const [isConnected, setIsConnected] = useState(false);
  const [latestEvent, setLatestEvent] = useState<GestureStreamEvent | null>(null);
  const [history, setHistory] = useState<GestureStreamEvent[]>([]);
  const clientRef = useRef<GestureStreamClient | null>(null);

  useEffect(() => {
    const client = new GestureStreamClient();
    clientRef.current = client;

    client.connect(
      (data) => {
        setLatestEvent(data);
        if (data.gesture && data.gesture !== 'UNKNOWN') {
          setHistory((prev) => [data, ...prev].slice(0, 50));
        }
      },
      (connected) => {
        setIsConnected(connected);
      }
    );

    return () => {
      client.disconnect();
    };
  }, []);

  return { isConnected, latestEvent, history };
}
