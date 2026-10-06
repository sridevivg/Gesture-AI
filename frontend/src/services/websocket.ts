import { GestureStreamEvent } from '@/types';

export class GestureStreamClient {
  private ws: WebSocket | null = null;
  private url: string;
  private onMessageCallback: ((data: GestureStreamEvent) => void) | null = null;
  private onStatusChangeCallback: ((connected: boolean) => void) | null = null;
  private reconnectTimer: number | null = null;

  constructor(url?: string) {
    this.url =
      url ||
      import.meta.env.VITE_WS_URL ||
      'ws://localhost:8000/api/v1/ws/gesture-stream';
  }

  connect(
    onMessage: (data: GestureStreamEvent) => void,
    onStatusChange?: (connected: boolean) => void
  ) {
    this.onMessageCallback = onMessage;
    this.onStatusChangeCallback = onStatusChange || null;

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        if (this.onStatusChangeCallback) this.onStatusChangeCallback(true);
      };

      this.ws.onmessage = (event) => {
        try {
          const parsed: GestureStreamEvent = JSON.parse(event.data);
          if (this.onMessageCallback) this.onMessageCallback(parsed);
        } catch (err) {
          console.error('Failed to parse incoming WebSocket message', err);
        }
      };

      this.ws.onclose = () => {
        if (this.onStatusChangeCallback) this.onStatusChangeCallback(false);
        this.scheduleReconnect();
      };

      this.ws.onerror = (err) => {
        console.warn('WebSocket connection error:', err);
        this.ws?.close();
      };
    } catch (err) {
      console.error('Error initiating WebSocket:', err);
      this.scheduleReconnect();
    }
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.reconnectTimer = window.setTimeout(() => {
      if (this.onMessageCallback) {
        this.connect(this.onMessageCallback, this.onStatusChangeCallback || undefined);
      }
    }, 3000);
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.onStatusChangeCallback) this.onStatusChangeCallback(false);
  }
}
