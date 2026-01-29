"""
Human Response Handler

Manages waiting for human input with timeouts and continuation logic.
"""

import asyncio
from typing import Optional, Callable
from datetime import datetime, timedelta


class HumanResponseHandler:
    """
    Handle waiting for human responses with intelligent timeout

    Features:
    - Configurable timeout for human response
    - Typing indicator detection
    - Automatic continuation if no response
    """

    def __init__(
        self,
        response_timeout: float = 30.0,  # 30 seconds default
        typing_grace_period: float = 10.0  # Additional 10s if typing detected
    ):
        """
        Initialize human response handler

        Args:
            response_timeout: Time to wait for human response (seconds)
            typing_grace_period: Extra time if human is typing (seconds)
        """
        self.response_timeout = response_timeout
        self.typing_grace_period = typing_grace_period
        self._is_typing = False
        self._typing_start = None

    def set_typing_state(self, is_typing: bool):
        """
        Update typing state

        Args:
            is_typing: Whether human is currently typing
        """
        if is_typing and not self._is_typing:
            self._typing_start = datetime.now()
        elif not is_typing and self._is_typing:
            self._typing_start = None

        self._is_typing = is_typing

    async def wait_for_human_response(
        self,
        check_for_response: Callable[[], Optional[str]],
        on_timeout: Optional[Callable[[], None]] = None
    ) -> Optional[str]:
        """
        Wait for human response with timeout

        Args:
            check_for_response: Async function that checks for new human message
            on_timeout: Optional callback when timeout occurs

        Returns:
            Human message if received, None if timeout
        """
        start_time = datetime.now()
        timeout_duration = self.response_timeout

        while True:
            # Check for response
            response = check_for_response()
            if response:
                return response

            # Calculate elapsed time
            elapsed = (datetime.now() - start_time).total_seconds()

            # If typing, extend timeout
            if self._is_typing:
                # Give extra time while typing
                effective_timeout = timeout_duration + self.typing_grace_period
            else:
                effective_timeout = timeout_duration

            # Check if timeout reached
            if elapsed >= effective_timeout:
                if on_timeout:
                    on_timeout()
                return None

            # Small sleep to avoid busy waiting
            await asyncio.sleep(0.5)

    async def wait_with_typing_check(
        self,
        timeout: float,
        typing_check: Callable[[], bool]
    ) -> bool:
        """
        Wait for timeout with periodic typing checks

        Args:
            timeout: Base timeout in seconds
            typing_check: Function that returns whether user is typing

        Returns:
            True if timeout completed, False if interrupted
        """
        start_time = datetime.now()
        effective_timeout = timeout

        while True:
            elapsed = (datetime.now() - start_time).total_seconds()

            # Check typing state
            is_typing = typing_check()
            self.set_typing_state(is_typing)

            # Extend timeout if typing started
            if is_typing and self._typing_start:
                typing_duration = (datetime.now() - self._typing_start).total_seconds()
                # Allow extra time for typing
                effective_timeout = timeout + self.typing_grace_period

            if elapsed >= effective_timeout:
                return True

            await asyncio.sleep(0.5)


# Global instance
human_response_handler = HumanResponseHandler()
