"""
OpenAI SDK Wrapper for Joule

Wraps the OpenAI Python SDK to automatically track usage.
"""

import time
from typing import Optional, Dict, Any

from .client import JouleClient, UsageEvent
from .pricing import get_openai_cost


class JouleOpenAI:
    """
    Wrapper around the OpenAI client that tracks usage to Joule.

    Usage:
        from openai import OpenAI
        from joule_sdk import JouleOpenAI

        client = OpenAI(api_key="sk-...")
        joule = JouleOpenAI(client, api_key="your-joule-key")

        # Use just like the regular OpenAI client
        response = joule.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """

    def __init__(
        self,
        openai_client,
        api_key: str,
        base_url: Optional[str] = None,
        user_id: Optional[str] = None,
        team_id: Optional[str] = None,
        application_id: Optional[str] = None,
        environment: Optional[str] = None,
        debug: bool = False
    ):
        self._openai = openai_client
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
        self.chat = _ChatWrapper(self._openai.chat, self._joule, self._debug)
        self.completions = _CompletionsWrapper(self._openai.completions, self._joule, self._debug)
        self.embeddings = _EmbeddingsWrapper(self._openai.embeddings, self._joule, self._debug)

    def close(self):
        """Close the Joule client."""
        self._joule.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class _ChatWrapper:
    """Wrapper for chat API."""

    def __init__(self, chat, joule: JouleClient, debug: bool):
        self._chat = chat
        self._joule = joule
        self._debug = debug
        self.completions = _ChatCompletionsWrapper(chat.completions, joule, debug)


class _ChatCompletionsWrapper:
    """Wrapper for chat.completions API."""

    def __init__(self, completions, joule: JouleClient, debug: bool):
        self._completions = completions
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
        Create a chat completion and track usage.

        Extra kwargs for Joule:
            joule_user_id: Override user ID for this request
            joule_team_id: Override team ID for this request
            joule_metadata: Additional metadata to track
        """
        start_time = time.time()

        try:
            response = self._completions.create(*args, **kwargs)
            elapsed_ms = int((time.time() - start_time) * 1000)

            # Extract usage from response
            if hasattr(response, 'usage') and response.usage:
                model = kwargs.get('model', response.model)
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                cost_cents = get_openai_cost(model, prompt_tokens, completion_tokens)

                event = UsageEvent(
                    provider="openai",
                    model=model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    cost_cents=cost_cents,
                    response_time_ms=elapsed_ms,
                    timestamp=start_time,
                    user_id=joule_user_id,
                    team_id=joule_team_id,
                    metadata=joule_metadata or {}
                )

                self._joule.track(event)

            return response

        except Exception as e:
            # Track failed requests too
            elapsed_ms = int((time.time() - start_time) * 1000)
            event = UsageEvent(
                provider="openai",
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


class _CompletionsWrapper:
    """Wrapper for legacy completions API."""

    def __init__(self, completions, joule: JouleClient, debug: bool):
        self._completions = completions
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
        """Create a completion and track usage."""
        start_time = time.time()

        try:
            response = self._completions.create(*args, **kwargs)
            elapsed_ms = int((time.time() - start_time) * 1000)

            if hasattr(response, 'usage') and response.usage:
                model = kwargs.get('model', response.model)
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens

                cost_cents = get_openai_cost(model, prompt_tokens, completion_tokens)

                event = UsageEvent(
                    provider="openai",
                    model=model,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    cost_cents=cost_cents,
                    response_time_ms=elapsed_ms,
                    timestamp=start_time,
                    user_id=joule_user_id,
                    team_id=joule_team_id,
                    metadata=joule_metadata or {}
                )

                self._joule.track(event)

            return response

        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            event = UsageEvent(
                provider="openai",
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


class _EmbeddingsWrapper:
    """Wrapper for embeddings API."""

    def __init__(self, embeddings, joule: JouleClient, debug: bool):
        self._embeddings = embeddings
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
        """Create embeddings and track usage."""
        start_time = time.time()

        try:
            response = self._embeddings.create(*args, **kwargs)
            elapsed_ms = int((time.time() - start_time) * 1000)

            if hasattr(response, 'usage') and response.usage:
                model = kwargs.get('model', response.model)
                total_tokens = response.usage.total_tokens

                cost_cents = get_openai_cost(model, total_tokens, 0)

                event = UsageEvent(
                    provider="openai",
                    model=model,
                    prompt_tokens=total_tokens,
                    completion_tokens=0,
                    total_tokens=total_tokens,
                    cost_cents=cost_cents,
                    response_time_ms=elapsed_ms,
                    timestamp=start_time,
                    user_id=joule_user_id,
                    team_id=joule_team_id,
                    metadata=joule_metadata or {}
                )

                self._joule.track(event)

            return response

        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            event = UsageEvent(
                provider="openai",
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
