"""Entry point for the SonarQube MCP server."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Literal


# Type alias for transport options (same as server.py)
TransportType = Literal["stdio", "sse", "streamable-http"]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="sonar-mcp",
        description="SonarQube MCP Server - Interact with SonarQube code quality platform",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default=os.environ.get("SONAR_MCP_TRANSPORT", "stdio"),
        help="Transport protocol (default: stdio, env: SONAR_MCP_TRANSPORT)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("SONAR_MCP_HOST", "127.0.0.1"),
        help="Host address for HTTP transports (default: 127.0.0.1, env: SONAR_MCP_HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("SONAR_MCP_PORT", "8000")),
        help="Port for HTTP transports (default: 8000, env: SONAR_MCP_PORT)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    return parser.parse_args()


def main() -> int:
    """Run the SonarQube MCP server.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    args = parse_args()

    if args.version:
        from sonar_mcp import __version__

        print(f"sonar-mcp {__version__}")
        return 0

    # Import here to avoid circular imports and allow --version to work without full init
    from sonar_mcp.server import create_server

    # Cast transport to the correct type
    transport: TransportType = args.transport

    # Create server with specified host/port (only used for HTTP transports)
    server = create_server(host=args.host, port=args.port)

    try:
        # Run the server with the specified transport
        server.run(transport=transport)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
