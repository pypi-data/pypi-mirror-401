"""
Joule API Client

Handles sending usage data to Joule servers.
"""

import time
import threading
import httpx
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class UsageEvent:
    """Represents a single API usage event."""
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_cents: float
    response_time_ms: int
    timestamp: float
    user_id: Optional[str] = None
    team_id: Optional[str] = None
    application_id: Optional[str] = None
    environment: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class JouleClient:
    """
    Client for sending usage data to Joule.

    Batches events and sends them asynchronously to minimize overhead.
    """

    DEFAULT_BASE_URL = "https://api.joule.ai"
    BATCH_SIZE = 10
    FLUSH_INTERVAL = 5.0  # seconds

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        user_id: Optional[str] = None,
        team_id: Optional[str] = None,
        application_id: Optional[str] = None,
        environment: Optional[str] = None,
        debug: bool = False
    ):
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.user_id = user_id
        self.team_id = team_id
        self.application_id = application_id
        self.environment = environment
        self.debug = debug

        self._queue: List[UsageEvent] = []
        self._lock = threading.Lock()
        self._timer: Optional[threading.Timer] = None
        self._http_client = httpx.Client(timeout=10.0)

        self._start_flush_timer()

    def _start_flush_timer(self):
        """Start the periodic flush timer."""
        self._timer = threading.Timer(self.FLUSH_INTERVAL, self._flush_timer_callback)
        self._timer.daemon = True
        self._timer.start()

    def _flush_timer_callback(self):
        """Called by timer to flush events."""
        self.flush()
        self._start_flush_timer()

    def track(self, event: UsageEvent):
        """
        Queue a usage event for sending to Joule.

        Events are batched and sent asynchronously.
        """
        # Apply defaults
        if not event.user_id:
            event.user_id = self.user_id
        if not event.team_id:
            event.team_id = self.team_id
        if not event.application_id:
            event.application_id = self.application_id
        if not event.environment:
            event.environment = self.environment

        with self._lock:
            self._queue.append(event)

            if len(self._queue) >= self.BATCH_SIZE:
                self._send_batch()

    def flush(self):
        """Send all queued events immediately."""
        with self._lock:
            if self._queue:
                self._send_batch()

    def _send_batch(self):
        """Send current batch of events. Must be called with lock held."""
        if not self._queue:
            return

        events = self._queue[:]
        self._queue = []

        # Send in background thread
        thread = threading.Thread(target=self._do_send, args=(events,))
        thread.daemon = True
        thread.start()

    def _do_send(self, events: List[UsageEvent]):
        """Actually send events to Joule API."""
        try:
            payload = {
                "events": [
                    {
                        "provider": e.provider,
                        "model": e.model,
                        "promptTokens": e.prompt_tokens,
                        "completionTokens": e.completion_tokens,
                        "totalTokens": e.total_tokens,
                        "costCents": e.cost_cents,
                        "responseTimeMs": e.response_time_ms,
                        "timestamp": e.timestamp,
                        "userId": e.user_id,
                        "teamId": e.team_id,
                        "applicationId": e.application_id,
                        "environment": e.environment,
                        "metadata": e.metadata,
                    }
                    for e in events
                ]
            }

            response = self._http_client.post(
                f"{self.base_url}/api/track/batch",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }
            )

            if self.debug:
                print(f"[Joule] Sent {len(events)} events, status: {response.status_code}")

            if response.status_code >= 400:
                if self.debug:
                    print(f"[Joule] Error response: {response.text}")

        except Exception as e:
            if self.debug:
                print(f"[Joule] Failed to send events: {e}")

    def close(self):
        """Flush remaining events and close the client."""
        if self._timer:
            self._timer.cancel()
        self.flush()
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
