"""SonarQube MCP Server.

A Model Context Protocol (MCP) server for interacting with SonarQube
code quality platform.
"""

from __future__ import annotations

import sys

import structlog


# Configure structlog to write to stderr instead of stdout.
# This is critical for MCP servers because stdout is used for JSON-RPC protocol
# messages. Any other output to stdout corrupts the protocol stream and causes
# "invalid trailing data at the end of stream" errors.
#
# We use WriteLoggerFactory (writes to stderr) with simple processors
# that don't require stdlib logger integration.
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
    cache_logger_on_first_use=True,
)

__version__ = "1.0.1"
__author__ = "Wade Woolwine"

__all__ = ["__version__"]
