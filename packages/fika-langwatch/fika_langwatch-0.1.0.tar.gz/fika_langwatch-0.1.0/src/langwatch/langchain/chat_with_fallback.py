"""
ChatWithFallback - LangChain chat model wrapper with automatic fallback and alerts.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Callable, Union, TYPE_CHECKING

from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult

from ..alerts.base import AlertChannel, AlertPayload
from ..key_manager import KeyManager, APIKey
from ..rate_limiter import InMemoryRateLimiter
from ..providers import ProviderFactory

if TYPE_CHECKING:
    from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


class ChatWithFallback(BaseChatModel):
    """
    LangChain-compatible chat model with automatic fallback and alert notifications.

    When a model fails, it automatically tries the next model in the chain.
    When all primary keys fail and fallback is activated, alerts are sent.

    Usage (Option A - bind_tools after creation):
        chat = ChatWithFallback.from_config(
            models=[
                {"name": "gemini-1", "provider": "google", "model": "gemini-2.5-flash", "api_key": "..."},
                {"name": "gemini-2", "provider": "google", "model": "gemini-2.5-flash", "api_key": "..."},
                {"name": "fallback", "provider": "openrouter", "model": "grok-4.1", "api_key": "...", "is_fallback": True},
            ],
            alerts=[EmailAlert(...), SlackAlert(...)],
        )

        # Bind tools - applies to ALL underlying models
        chat_with_tools = chat.bind_tools([tool1, tool2])
        response = await chat_with_tools.ainvoke(messages)

    Usage (Manual models):
        chat = ChatWithFallback(
            models=[model1, model2, fallback_model],
            model_names=["gemini-1", "gemini-2", "fallback"],
            alerts=[EmailAlert(...)],
        )
    """

    # Pydantic fields
    models: List[BaseChatModel] = []
    key_manager: Optional[KeyManager] = None
    alerts: List[AlertChannel] = []
    rate_limiter: InMemoryRateLimiter = None
    cooldown_seconds: int = 3600
    model_names: List[str] = []
    on_key_failure: Optional[Callable] = None
    on_fallback_activated: Optional[Callable] = None
    _fallback_alert_sent: bool = False

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        models: List[BaseChatModel],
        model_names: Optional[List[str]] = None,
        alerts: Optional[List[AlertChannel]] = None,
        key_manager: Optional[KeyManager] = None,
        rate_limiter: Optional[InMemoryRateLimiter] = None,
        cooldown_seconds: int = 3600,
        on_key_failure: Optional[Callable] = None,
        on_fallback_activated: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Initialize ChatWithFallback.

        Args:
            models: List of LangChain chat models (primary + fallbacks)
            model_names: Names for each model (for alerts). Auto-generated if not provided.
            alerts: List of alert channels (Email, Slack, Webhook)
            key_manager: Optional KeyManager for detailed health tracking
            rate_limiter: Optional rate limiter (created automatically if not provided)
            cooldown_seconds: Cooldown between alerts (default: 3600 = 1 hour)
            on_key_failure: Optional callback when a key fails: fn(key_name, error)
            on_fallback_activated: Optional callback when fallback activates: fn(fallback_key_name)
        """
        super().__init__(**kwargs)

        self.models = models
        self.model_names = model_names or [f"model-{i}" for i in range(len(models))]
        self.alerts = alerts or []
        self.key_manager = key_manager
        self.rate_limiter = rate_limiter or InMemoryRateLimiter(default_cooldown=cooldown_seconds)
        self.cooldown_seconds = cooldown_seconds
        self.on_key_failure = on_key_failure
        self.on_fallback_activated = on_fallback_activated
        self._fallback_alert_sent = False

        if len(self.model_names) != len(self.models):
            raise ValueError(f"model_names length ({len(self.model_names)}) must match models length ({len(self.models)})")

        logger.info(f"ChatWithFallback initialized with {len(models)} models: {self.model_names}")

    @classmethod
    def from_config(
        cls,
        models: List[Dict[str, Any]],
        alerts: Optional[List[AlertChannel]] = None,
        cooldown_seconds: int = 3600,
        on_key_failure: Optional[Callable] = None,
        on_fallback_activated: Optional[Callable] = None,
    ) -> "ChatWithFallback":
        """
        Create ChatWithFallback from configuration dictionaries.

        Args:
            models: List of model configs with keys: name, provider, model, api_key, is_fallback
            alerts: List of alert channels
            cooldown_seconds: Cooldown between alerts
            on_key_failure: Callback when key fails
            on_fallback_activated: Callback when fallback activates

        Returns:
            ChatWithFallback instance

        Example:
            chat = ChatWithFallback.from_config(
                models=[
                    {"name": "gemini-1", "provider": "google", "model": "gemini-2.5-flash", "api_key": "AIza..."},
                    {"name": "fallback", "provider": "openrouter", "model": "grok-4.1", "api_key": "sk-...", "is_fallback": True},
                ],
                alerts=[EmailAlert(...), SlackAlert(...)],
            )
        """
        # Create KeyManager
        key_manager = KeyManager([
            {
                "name": m["name"],
                "key": m["api_key"],
                "provider": m["provider"],
                "model": m["model"],
                "is_fallback": m.get("is_fallback", False),
                "extra_config": m.get("extra_config", {}),
            }
            for m in models
        ])

        # Create LangChain models using factory
        langchain_models = []
        for key in key_manager.keys:
            model = ProviderFactory.create_model(key)
            langchain_models.append(model)

        model_names = [m["name"] for m in models]

        return cls(
            models=langchain_models,
            model_names=model_names,
            alerts=alerts,
            key_manager=key_manager,
            cooldown_seconds=cooldown_seconds,
            on_key_failure=on_key_failure,
            on_fallback_activated=on_fallback_activated,
        )

    def bind_tools(
        self,
        tools: Sequence["BaseTool"],
        **kwargs,
    ) -> "ChatWithFallback":
        """
        Bind tools to ALL underlying models and return a new ChatWithFallback.

        Args:
            tools: Sequence of tools to bind
            **kwargs: Additional arguments passed to each model's bind_tools

        Returns:
            New ChatWithFallback with tools bound to all models
        """
        # Bind tools to each model
        bound_models = []
        for model in self.models:
            if hasattr(model, "bind_tools"):
                bound_model = model.bind_tools(tools, **kwargs)
                bound_models.append(bound_model)
            else:
                logger.warning(f"Model {type(model).__name__} does not support bind_tools")
                bound_models.append(model)

        # Create new instance with bound models
        return ChatWithFallback(
            models=bound_models,
            model_names=self.model_names,
            alerts=self.alerts,
            key_manager=self.key_manager,
            rate_limiter=self.rate_limiter,
            cooldown_seconds=self.cooldown_seconds,
            on_key_failure=self.on_key_failure,
            on_fallback_activated=self.on_fallback_activated,
        )

    @property
    def _llm_type(self) -> str:
        return "chat_with_fallback"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_names": self.model_names,
            "num_models": len(self.models),
        }

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> ChatResult:
        """Synchronous generation with fallback."""
        last_error = None

        for i, model in enumerate(self.models):
            model_name = self.model_names[i]
            is_fallback = self.key_manager and self.key_manager.keys[i].is_fallback if self.key_manager else (i == len(self.models) - 1)

            try:
                logger.debug(f"Trying model: {model_name}")
                result = model._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

                # Mark as healthy if we have key_manager
                if self.key_manager:
                    self.key_manager.mark_healthy(model_name)

                return result

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Model {model_name} failed: {last_error[:100]}")

                # Track failure
                self._handle_failure(i, model_name, last_error, is_fallback)

        # All models failed
        raise RuntimeError(f"All {len(self.models)} models failed. Last error: {last_error}")

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> ChatResult:
        """Asynchronous generation with fallback."""
        last_error = None

        for i, model in enumerate(self.models):
            model_name = self.model_names[i]
            is_fallback = self.key_manager and self.key_manager.keys[i].is_fallback if self.key_manager else (i == len(self.models) - 1)

            try:
                logger.debug(f"Trying model: {model_name}")
                result = await model._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)

                # Mark as healthy
                if self.key_manager:
                    self.key_manager.mark_healthy(model_name)

                return result

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Model {model_name} failed: {last_error[:100]}")

                # Track failure
                await self._handle_failure_async(i, model_name, last_error, is_fallback)

        # All models failed
        raise RuntimeError(f"All {len(self.models)} models failed. Last error: {last_error}")

    def _handle_failure(self, index: int, model_name: str, error: str, is_fallback: bool) -> None:
        """Handle model failure synchronously."""
        # Mark as failed in key manager
        if self.key_manager:
            self.key_manager.mark_failed_by_index(index, error)

        # Callback
        if self.on_key_failure:
            try:
                self.on_key_failure(model_name, error)
            except Exception as e:
                logger.error(f"on_key_failure callback error: {e}")

        # Check if we should send fallback alert
        if not is_fallback and self._should_send_fallback_alert(index):
            self._send_alerts_sync(index, model_name, error)

    async def _handle_failure_async(self, index: int, model_name: str, error: str, is_fallback: bool) -> None:
        """Handle model failure asynchronously."""
        # Mark as failed in key manager
        if self.key_manager:
            self.key_manager.mark_failed_by_index(index, error)

        # Callback
        if self.on_key_failure:
            try:
                self.on_key_failure(model_name, error)
            except Exception as e:
                logger.error(f"on_key_failure callback error: {e}")

        # Check if we should send fallback alert (when last primary key fails)
        if not is_fallback and self._should_send_fallback_alert(index):
            await self._send_alerts_async(index, model_name, error)

    def _should_send_fallback_alert(self, failed_index: int) -> bool:
        """Check if we should send fallback alert."""
        # Find the next model
        next_index = failed_index + 1
        if next_index >= len(self.models):
            return False

        # Check if next model is a fallback
        if self.key_manager:
            next_key = self.key_manager.keys[next_index]
            return next_key.is_fallback
        else:
            # Without key_manager, assume last model is fallback
            return next_index == len(self.models) - 1

    def _send_alerts_sync(self, failed_index: int, model_name: str, error: str) -> None:
        """Send alerts synchronously."""
        alert_key = "fallback_activated"

        # Check rate limit
        if not self.rate_limiter.can_send(alert_key, self.cooldown_seconds):
            logger.debug("Alert in cooldown, skipping")
            return

        # Get fallback info
        fallback_name = None
        fallback_provider = None
        if failed_index + 1 < len(self.models):
            fallback_name = self.model_names[failed_index + 1]
            if self.key_manager:
                fallback_key = self.key_manager.keys[failed_index + 1]
                fallback_provider = fallback_key.provider

        # Build payload
        payload = self._build_alert_payload(model_name, error, fallback_name, fallback_provider)

        # Send to all channels
        for channel in self.alerts:
            try:
                channel.send(payload)
            except Exception as e:
                logger.error(f"Failed to send alert via {channel.name}: {e}")

        # Mark sent
        self.rate_limiter.mark_sent(alert_key, self.cooldown_seconds)

        # Callback
        if self.on_fallback_activated and fallback_name:
            try:
                self.on_fallback_activated(fallback_name)
            except Exception as e:
                logger.error(f"on_fallback_activated callback error: {e}")

    async def _send_alerts_async(self, failed_index: int, model_name: str, error: str) -> None:
        """Send alerts asynchronously."""
        alert_key = "fallback_activated"

        # Check rate limit
        if not self.rate_limiter.can_send(alert_key, self.cooldown_seconds):
            logger.debug("Alert in cooldown, skipping")
            return

        # Get fallback info
        fallback_name = None
        fallback_provider = None
        if failed_index + 1 < len(self.models):
            fallback_name = self.model_names[failed_index + 1]
            if self.key_manager:
                fallback_key = self.key_manager.keys[failed_index + 1]
                fallback_provider = fallback_key.provider

        # Build payload
        payload = self._build_alert_payload(model_name, error, fallback_name, fallback_provider)

        # Send to all channels concurrently
        tasks = [channel.send_async(payload) for channel in self.alerts]
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to send alert via {self.alerts[i].name}: {result}")

        # Mark sent
        self.rate_limiter.mark_sent(alert_key, self.cooldown_seconds)

        # Callback
        if self.on_fallback_activated and fallback_name:
            try:
                self.on_fallback_activated(fallback_name)
            except Exception as e:
                logger.error(f"on_fallback_activated callback error: {e}")

    def _build_alert_payload(
        self,
        failed_model_name: str,
        error: str,
        fallback_name: Optional[str],
        fallback_provider: Optional[str],
    ) -> AlertPayload:
        """Build alert payload."""
        failed_provider = None
        if self.key_manager:
            key = self.key_manager.get_key_by_name(failed_model_name)
            if key:
                failed_provider = key.provider

        # Get all failed keys for message
        failed_keys = []
        if self.key_manager:
            failed_keys = self.key_manager.get_failed_key_names()

        message = f"All primary API keys have failed. System is now using fallback: {fallback_name or 'unknown'}."
        if failed_keys:
            message += f" Failed keys: {', '.join(failed_keys)}."

        return AlertPayload(
            title=f"API Key Failure - Fallback Activated",
            message=message,
            severity="critical",
            alert_type="fallback_activated",
            timestamp=datetime.now(),
            details={
                "failed_keys": failed_keys,
                "fallback": fallback_name,
            },
            failed_key_name=failed_model_name,
            failed_provider=failed_provider,
            fallback_key_name=fallback_name,
            fallback_provider=fallback_provider,
            error_message=error,
        )

    def get_status(self) -> Dict[str, Any]:
        """Get current status of all models."""
        if self.key_manager:
            return self.key_manager.get_status_summary()
        return {
            "model_names": self.model_names,
            "num_models": len(self.models),
        }
