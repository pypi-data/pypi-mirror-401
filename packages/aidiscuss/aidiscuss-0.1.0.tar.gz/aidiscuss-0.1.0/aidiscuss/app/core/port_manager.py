"""
Port Management Utility
Securely discovers and manages available ports for the application
"""

import socket
from typing import Optional


def is_port_available(host: str, port: int) -> bool:
    """
    Check if a port is available for binding.

    Args:
        host: Host address to check (e.g., '127.0.0.1')
        port: Port number to check

    Returns:
        True if port is available, False otherwise
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            return True
    except OSError:
        return False


def find_available_port(
    preferred_port: int = 8000,
    host: str = "127.0.0.1",
    port_range: tuple[int, int] = (8000, 8100)
) -> Optional[int]:
    """
    Find an available port, preferring the specified port.

    Security considerations:
    - Binds to localhost (127.0.0.1) only, not 0.0.0.0
    - Uses specific port range to avoid system/privileged ports
    - Checks preferred port first to maintain consistency
    - Falls back to OS-assigned port if range exhausted

    Args:
        preferred_port: First port to try
        host: Host address (default: 127.0.0.1 for localhost-only)
        port_range: Range of ports to try (default: 8000-8100)

    Returns:
        Available port number, or None if no port found
    """
    # Try preferred port first
    if port_range[0] <= preferred_port <= port_range[1]:
        if is_port_available(host, preferred_port):
            return preferred_port

    # Try other ports in range
    for port in range(port_range[0], port_range[1] + 1):
        if port == preferred_port:
            continue  # Already tried
        if is_port_available(host, port):
            return port

    # Last resort: let OS assign a free port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, 0))  # Port 0 = OS picks free port
            return sock.getsockname()[1]
    except OSError:
        return None


def get_server_port(preferred_port: Optional[int] = None, host: str = "127.0.0.1") -> int:
    """
    Get an available port for the server, with fallback logic.

    Args:
        preferred_port: Preferred port (from env or config)
        host: Host address

    Returns:
        Available port number

    Raises:
        RuntimeError: If no port could be found
    """
    preferred = preferred_port or 8000
    port = find_available_port(preferred_port=preferred, host=host)

    if port is None:
        raise RuntimeError(
            "Could not find an available port. "
            "Please ensure ports 8000-8100 are not all in use."
        )

    return port
