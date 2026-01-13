"""
Token tracker singleton for monitoring token usage across all agent calls.

This module provides a thread-safe singleton class that tracks token usage
over time and calculates tokens per minute (TPM) using a sliding window approach.
"""

import threading
import time
from collections import deque
from typing import Optional


class TokenTracker:
    """
    Singleton class to track token usage per minute across all agent calls.

    This class maintains a sliding window of token usage over time and can calculate
    the current tokens per minute (TPM) rate. It uses a 60-second sliding window
    to provide accurate real-time TPM measurements.

    Thread-safe implementation using locks for concurrent access.

    Example:
        >>> tracker = TokenTracker()
        >>> tracker.add_tokens(100)
        >>> tpm = tracker.get_tokens_per_minute()
        >>> print(f"Current TPM: {tpm:.2f}")
    """

    _instance: Optional["TokenTracker"] = None
    _lock = threading.Lock()

    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            with cls._lock:
                # Double-check locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the token tracker (only runs once)."""
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._initialized = True
        self._token_history: deque = deque()  # (timestamp, token_count) tuples
        self._history_lock = threading.Lock()
        self._window_seconds = 60  # 1 minute window for TPM calculation

    def add_tokens(self, count: int) -> None:
        """
        Add token usage at the current timestamp.

        Args:
            count: Number of tokens to add
        """
        if count <= 0:
            return

        with self._history_lock:
            current_time = time.time()
            self._token_history.append((current_time, count))
            self._cleanup_old_entries(current_time)

    def get_tokens_per_minute(self) -> float:
        """
        Calculate current tokens per minute based on sliding window.

        Returns:
            The current TPM rate as a float. Returns 0.0 if no tokens tracked.

        Note:
            This uses a sliding 60-second window. If there's only one data point,
            it assumes that represents the full minute rate.
        """
        with self._history_lock:
            current_time = time.time()
            self._cleanup_old_entries(current_time)

            if not self._token_history:
                return 0.0

            # Sum all tokens in the window
            total_tokens = sum(count for _, count in self._token_history)

            # Calculate actual time span
            if len(self._token_history) == 1:
                # If only one entry, assume it represents the full minute rate
                return float(total_tokens)

            oldest_time = self._token_history[0][0]
            time_span = current_time - oldest_time

            if time_span == 0:
                return float(total_tokens)

            # Normalize to per-minute rate
            tokens_per_minute = (total_tokens / time_span) * 60
            return tokens_per_minute

    def get_total_tokens(self) -> int:
        """
        Get total tokens in current window.

        Returns:
            Sum of all tokens tracked within the sliding window
        """
        with self._history_lock:
            current_time = time.time()
            self._cleanup_old_entries(current_time)
            return sum(count for _, count in self._token_history)

    def get_token_count(self) -> int:
        """
        Get the number of token entries in the current window.

        Returns:
            Number of separate token usage events tracked
        """
        with self._history_lock:
            current_time = time.time()
            self._cleanup_old_entries(current_time)
            return len(self._token_history)

    def reset(self) -> None:
        """Clear all tracked tokens."""
        with self._history_lock:
            self._token_history.clear()

    def get_stats(self) -> dict:
        """
        Get comprehensive statistics about current token usage.

        Returns:
            Dictionary containing:
                - tokens_per_minute: Current TPM rate
                - total_tokens: Total tokens in window
                - entry_count: Number of API calls in window
                - window_seconds: Size of tracking window
        """
        with self._history_lock:
            current_time = time.time()
            self._cleanup_old_entries(current_time)

            total_tokens = sum(count for _, count in self._token_history)

            if not self._token_history:
                tpm = 0.0
            elif len(self._token_history) == 1:
                tpm = float(total_tokens)
            else:
                oldest_time = self._token_history[0][0]
                time_span = current_time - oldest_time
                tpm = (total_tokens / time_span * 60) if time_span > 0 else float(total_tokens)

            return {
                "tokens_per_minute": tpm,
                "total_tokens": total_tokens,
                "entry_count": len(self._token_history),
                "window_seconds": self._window_seconds,
            }

    def _cleanup_old_entries(self, current_time: float) -> None:
        """
        Remove entries older than the sliding window.

        Args:
            current_time: Current timestamp to compare against
        """
        cutoff_time = current_time - self._window_seconds
        while self._token_history and self._token_history[0][0] < cutoff_time:
            self._token_history.popleft()
