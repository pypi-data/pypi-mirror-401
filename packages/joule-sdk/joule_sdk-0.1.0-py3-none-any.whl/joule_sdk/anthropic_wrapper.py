"""
Anthropic SDK Wrapper for Joule

Wraps the Anthropic Python SDK to automatically track usage.
"""

import time
from typing import Optional, Dict, Any

from .client import JouleClient, UsageEvent
from .pricing import get_anthropic_cost


class JouleAnthropic:
    """
    Wrapper around the Anthropic client that tracks usage to Joule.

    Usage:
        from anthropic import Anthropic
        from joule_sdk import JouleAnthropic

        client = Anthropic(api_key="sk-ant-...")
        joule = JouleAnthropic(client, api_key="your-joule-key")

        # Use just like the regular Anthropic client
        response = joule.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """

    def __init__(
        self,
        anthropic_client,
        api_key: str,
        base_url: Optional[str] = None,
        user_id: Optional[str] = None,
        team_id: Optional[str] = None,
        application_id: Optional[str] = None,
        environment: Optional[str] = None,
        debug: bool = False
    ):
        self._anthropic = anthropic_client
        self._joule = JouleClient(
            api_key=api_key,
            base_url=base_url,
            user_id=user_id,
            team_id=team_id,
            application_id=application_id,
            environment=environment,
            debug=debug
        )
        self._debug = debug

        # Create wrapped API access
        self.messages = _MessagesWrapper(self._anthropic.messages, self._joule, self._debug)

    def close(self):
        """Close the Joule client."""
        self._joule.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class _MessagesWrapper:
    """Wrapper for messages API."""

    def __init__(self, messages, joule: JouleClient, debug: bool):
        self._messages = messages
        self._joule = joule
        self._debug = debug

    def create(
        self,
        *args,
        joule_user_id: Optional[str] = None,
        joule_team_id: Optional[str] = None,
        joule_metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Create a message and track usage.

        Extra kwargs for Joule:
            joule_user_id: Override user ID for this request
            joule_team_id: Override team ID for this request
            joule_metadata: Additional metadata to track
        """
        start_time = time.time()

        try:
            response = self._messages.create(*args, **kwargs)
            elapsed_ms = int((time.time() - start_time) * 1000)

            # Extract usage from response
            if hasattr(response, 'usage') and response.usage:
                model = kwargs.get('model', response.model)
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens

                # Handle cache tokens if present
                cache_read = getattr(response.usage, 'cache_read_input_tokens', 0) or 0
                cache_creation = getattr(response.usage, 'cache_creation_input_tokens', 0) or 0

                cost_cents = get_anthropic_cost(
                    model,
                    input_tokens,
                    output_tokens,
                    cache_read,
                    cache_creation
                )

                event = UsageEvent(
                    provider="anthropic",
                    model=model,
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    cost_cents=cost_cents,
                    response_time_ms=elapsed_ms,
                    timestamp=start_time,
                    user_id=joule_user_id,
                    team_id=joule_team_id,
                    metadata={
                        **(joule_metadata or {}),
                        "cache_read_tokens": cache_read,
                        "cache_creation_tokens": cache_creation,
                    }
                )

                self._joule.track(event)

            return response

        except Exception as e:
            # Track failed requests too
            elapsed_ms = int((time.time() - start_time) * 1000)
            event = UsageEvent(
                provider="anthropic",
                model=kwargs.get('model', 'unknown'),
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                cost_cents=0,
                response_time_ms=elapsed_ms,
                timestamp=start_time,
                user_id=joule_user_id,
                team_id=joule_team_id,
                metadata={
                    **(joule_metadata or {}),
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            self._joule.track(event)
            raise

    def stream(
        self,
        *args,
        joule_user_id: Optional[str] = None,
        joule_team_id: Optional[str] = None,
        joule_metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Stream a message and track usage.

        Returns a context manager that yields message events.
        """
        start_time = time.time()

        try:
            # Get the stream
            stream = self._messages.stream(*args, **kwargs)

            # Return a wrapper that tracks usage when stream completes
            return _StreamWrapper(
                stream,
                self._joule,
                kwargs.get('model', 'unknown'),
                start_time,
                joule_user_id,
                joule_team_id,
                joule_metadata
            )

        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            event = UsageEvent(
                provider="anthropic",
                model=kwargs.get('model', 'unknown'),
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                cost_cents=0,
                response_time_ms=elapsed_ms,
                timestamp=start_time,
                user_id=joule_user_id,
                team_id=joule_team_id,
                metadata={
                    **(joule_metadata or {}),
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            self._joule.track(event)
            raise


class _StreamWrapper:
    """Wrapper for streaming responses that tracks usage on completion."""

    def __init__(
        self,
        stream,
        joule: JouleClient,
        model: str,
        start_time: float,
        user_id: Optional[str],
        team_id: Optional[str],
        metadata: Optional[Dict[str, Any]]
    ):
        self._stream = stream
        self._joule = joule
        self._model = model
        self._start_time = start_time
        self._user_id = user_id
        self._team_id = team_id
        self._metadata = metadata or {}

    def __enter__(self):
        self._stream.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = self._stream.__exit__(exc_type, exc_val, exc_tb)

        # Track usage after stream completes
        elapsed_ms = int((time.time() - self._start_time) * 1000)

        # Try to get final message with usage
        try:
            final_message = self._stream.get_final_message()
            if hasattr(final_message, 'usage') and final_message.usage:
                input_tokens = final_message.usage.input_tokens
                output_tokens = final_message.usage.output_tokens

                cache_read = getattr(final_message.usage, 'cache_read_input_tokens', 0) or 0
                cache_creation = getattr(final_message.usage, 'cache_creation_input_tokens', 0) or 0

                cost_cents = get_anthropic_cost(
                    self._model,
                    input_tokens,
                    output_tokens,
                    cache_read,
                    cache_creation
                )

                event = UsageEvent(
                    provider="anthropic",
                    model=self._model,
                    prompt_tokens=input_tokens,
                    completion_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    cost_cents=cost_cents,
                    response_time_ms=elapsed_ms,
                    timestamp=self._start_time,
                    user_id=self._user_id,
                    team_id=self._team_id,
                    metadata={
                        **self._metadata,
                        "streaming": True,
                        "cache_read_tokens": cache_read,
                        "cache_creation_tokens": cache_creation,
                    }
                )

                self._joule.track(event)

        except Exception:
            # If we can't get usage, just skip tracking
            pass

        return result

    def __iter__(self):
        return iter(self._stream)

    @property
    def text_stream(self):
        return self._stream.text_stream

    def get_final_message(self):
        return self._stream.get_final_message()

    def get_final_text(self):
        return self._stream.get_final_text()
