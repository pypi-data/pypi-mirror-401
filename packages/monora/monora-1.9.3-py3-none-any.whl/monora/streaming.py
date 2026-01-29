"""Callback-based event subscription for real-time monitoring.

Provides a pub/sub interface for subscribing to Monora events as they're emitted.
"""
from __future__ import annotations

import fnmatch
import threading
import uuid
from typing import Any, Callable, Dict, List, Optional, Set

# Type alias for event callbacks
EventCallback = Callable[[Dict[str, Any]], None]


class EventSubscription:
    """Represents a single event subscription."""

    def __init__(
        self,
        callback: EventCallback,
        filters: Optional[Dict[str, Any]] = None,
        subscription_id: Optional[str] = None,
    ):
        self.id = subscription_id or f"sub_{uuid.uuid4().hex[:12]}"
        self.callback = callback
        self.filters = filters or {}
        self.active = True

    def matches(self, event: Dict[str, Any]) -> bool:
        """Check if an event matches this subscription's filters."""
        if not self.active:
            return False

        for key, pattern in self.filters.items():
            event_value = event.get(key)
            if event_value is None:
                return False

            # Support glob patterns for string values
            if isinstance(pattern, str) and isinstance(event_value, str):
                if not fnmatch.fnmatch(event_value, pattern):
                    return False
            # Support list of allowed values
            elif isinstance(pattern, (list, tuple, set)):
                if event_value not in pattern:
                    return False
            # Direct equality check
            elif event_value != pattern:
                return False

        return True

    def cancel(self) -> None:
        """Cancel this subscription."""
        self.active = False


class EventBus:
    """Central event bus for managing subscriptions and dispatching events."""

    def __init__(self):
        self._subscriptions: Dict[str, EventSubscription] = {}
        self._lock = threading.Lock()

    def subscribe(
        self,
        callback: EventCallback,
        filters: Optional[Dict[str, Any]] = None,
    ) -> EventSubscription:
        """Subscribe to events with optional filtering.

        Args:
            callback: Function to call when matching event is emitted.
                      Signature: callback(event: Dict[str, Any]) -> None
            filters: Optional filters to match events. Supports:
                     - event_type: Match event type (supports glob patterns)
                     - trace_id: Match specific trace
                     - data_classification: Match classification level
                     - Any other event field

        Returns:
            EventSubscription object that can be used to cancel the subscription

        Example:
            # Subscribe to all LLM calls
            sub = monora.subscribe(
                lambda e: print(f"LLM call: {e['body'].get('model')}"),
                filters={"event_type": "llm_call"}
            )

            # Subscribe to specific trace
            sub = monora.subscribe(my_handler, filters={"trace_id": "trc_abc123"})

            # Subscribe to multiple event types
            sub = monora.subscribe(
                handler,
                filters={"event_type": ["llm_call", "tool_call"]}
            )

            # Cancel subscription
            sub.cancel()
        """
        subscription = EventSubscription(callback, filters)
        with self._lock:
            self._subscriptions[subscription.id] = subscription
        return subscription

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription by ID.

        Args:
            subscription_id: The subscription ID to remove

        Returns:
            True if subscription was found and removed, False otherwise
        """
        with self._lock:
            if subscription_id in self._subscriptions:
                self._subscriptions[subscription_id].cancel()
                del self._subscriptions[subscription_id]
                return True
            return False

    def publish(self, event: Dict[str, Any]) -> int:
        """Publish an event to all matching subscribers.

        Args:
            event: The event to publish

        Returns:
            Number of subscribers that received the event
        """
        # Get snapshot of active subscriptions
        with self._lock:
            subscriptions = list(self._subscriptions.values())

        notified = 0
        for subscription in subscriptions:
            if subscription.matches(event):
                try:
                    subscription.callback(event)
                    notified += 1
                except Exception:
                    # Don't let subscriber errors break the event flow
                    pass

        return notified

    def clear(self) -> int:
        """Remove all subscriptions.

        Returns:
            Number of subscriptions removed
        """
        with self._lock:
            count = len(self._subscriptions)
            for sub in self._subscriptions.values():
                sub.cancel()
            self._subscriptions.clear()
            return count

    def get_subscription_count(self) -> int:
        """Get the number of active subscriptions."""
        with self._lock:
            return sum(1 for sub in self._subscriptions.values() if sub.active)

    def get_subscription_ids(self) -> List[str]:
        """Get list of active subscription IDs."""
        with self._lock:
            return [
                sub_id
                for sub_id, sub in self._subscriptions.items()
                if sub.active
            ]


# Global event bus instance
_event_bus: Optional[EventBus] = None
_event_bus_lock = threading.Lock()


def get_event_bus() -> EventBus:
    """Get or create the global event bus."""
    global _event_bus
    if _event_bus is None:
        with _event_bus_lock:
            if _event_bus is None:
                _event_bus = EventBus()
    return _event_bus


def subscribe(
    callback: EventCallback,
    filters: Optional[Dict[str, Any]] = None,
) -> EventSubscription:
    """Subscribe to Monora events with optional filtering.

    This is the main public API for event subscription.

    Args:
        callback: Function to call when matching event is emitted
        filters: Optional filters to match events

    Returns:
        EventSubscription object for managing the subscription

    Example:
        import monora

        # Subscribe to all LLM calls
        def on_llm_call(event):
            model = event.get("body", {}).get("model", "unknown")
            print(f"LLM call to {model}")

        sub = monora.subscribe(on_llm_call, filters={"event_type": "llm_call"})

        # Later: cancel subscription
        sub.cancel()
    """
    return get_event_bus().subscribe(callback, filters)


def unsubscribe(subscription_id: str) -> bool:
    """Remove a subscription by ID.

    Args:
        subscription_id: The subscription ID to remove

    Returns:
        True if subscription was found and removed
    """
    return get_event_bus().unsubscribe(subscription_id)


def publish_event(event: Dict[str, Any]) -> int:
    """Publish an event to all subscribers (internal use).

    This is called by the runtime when events are emitted.

    Args:
        event: The event to publish

    Returns:
        Number of subscribers notified
    """
    return get_event_bus().publish(event)


def clear_subscriptions() -> int:
    """Clear all event subscriptions.

    Returns:
        Number of subscriptions cleared
    """
    return get_event_bus().clear()
