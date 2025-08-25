import os
import platform
import socket
import subprocess
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastmcp import FastMCP
from pydantic import BaseModel, field_validator

from app.config import settings
from app.logger import logger

# Create MCP server
mcp = FastMCP(name=settings.server_name)

# Track server start time
SERVER_START_TIME = time.time()

logger.info("MCP server initialized", extra={"tool_name": "system"})


# Input validation for time_now tool
class TimeRequest(BaseModel):
    """Input validation model for time_now tool."""

    tz: str

    @field_validator("tz")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone parameter."""
        # Supported timezones
        valid_timezones = ["UTC", "GMT", "EST", "PST", "IST", "CET"]

        # Convert to uppercase for comparison
        tz_upper = v.upper()

        if tz_upper not in valid_timezones:
            raise ValueError(
                f"Timezone '{v}' not supported. "
                f"Valid options: {', '.join(valid_timezones)}"
            )

        return tz_upper


# Pure functions (not wrapped by FastMCP)
def _ping():
    """Internal ping function."""
    start_time = time.time()
    logger.info("Ping tool called", extra={"tool_name": "ping"})

    result = {
        "message": "pong",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success",
    }

    execution_time = (time.time() - start_time) * 1000  # Convert to ms
    logger.info(
        "Ping completed successfully",
        extra={"tool_name": "ping", "execution_time": execution_time},
    )

    return result


def _whoami():
    """Internal whoami function."""
    logger.info("Whoami tool called", extra={"tool_name": "whoami"})

    try:
        result = {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "username": os.getenv("USER") or os.getenv("USERNAME", "unknown"),
            "app_env": settings.app_env,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
        }

        logger.info("Whoami completed successfully", extra={"tool_name": "whoami"})

        return result

    except Exception as e:
        logger.error(f"Whoami failed: {e}", extra={"tool_name": "whoami"})
        return {"error": str(e), "status": "failed"}


def _time_now(tz: str) -> Dict[str, Any]:
    """Internal time_now function with pure logic."""
    start_time = time.time()
    logger.info("time_now requested", extra={"tool_name": "time_now"})

    try:
        # Timezone offset mapping (hours from UTC)
        timezone_offsets = {
            "UTC": 0,
            "GMT": 0,
            "EST": -5,  # Eastern Standard Time
            "PST": -8,  # Pacific Standard Time
            "IST": 5.5,  # India Standard Time (UTC+5:30)
            "CET": 1,  # Central European Time
        }

        # Get current UTC time
        utc_now = datetime.now(timezone.utc)

        # Calculate local time in requested timezone
        offset_hours = timezone_offsets[tz]
        local_time = utc_now + timedelta(hours=offset_hours)

        result = {
            "timezone": tz,
            "utc_time": utc_now.isoformat(),
            "local_time": local_time.isoformat(),
            "formatted": local_time.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": local_time.strftime("%A"),
            "offset_hours": offset_hours,
            "status": "success",
        }

        execution_time = (time.time() - start_time) * 1000
        logger.info(
            "Time_Now completed successfully",
            extra={"tool_name": "time_now", "execution_time": execution_time},
        )

        return result

    except Exception as e:
        logger.error(f"Time_Now failed: {e}", extra={"tool_name": "time_now"})
        return {"error": str(e), "status": "failed", "timezone": tz}


def _health_check() -> Dict[str, Any]:
    """Internal health_check function with pure logic."""
    start_time = time.time()
    logger.info("Health check requested", extra={"tool_name": "health_check"})

    try:
        # Calculate uptime
        uptime_seconds = time.time() - SERVER_START_TIME

        # Get git SHA (simplified)
        git_sha = "unknown"
        try:
            git_sha = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
        except Exception:
            pass  # Git not available

        result = {
            "status": "healthy",
            "version": "0.1.0",
            "git_sha": git_sha,
            "uptime_seconds": round(uptime_seconds, 2),
            "uptime_formatted": f"{uptime_seconds:.1f} seconds"
            if uptime_seconds < 60
            else f"{uptime_seconds / 60:.1f} minutes",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        execution_time = (time.time() - start_time) * 1000
        logger.info(
            "Health check completed successfully",
            extra={"tool_name": "health_check", "execution_time": execution_time},
        )

        return result

    except Exception as e:
        logger.error(f"Health check failed: {e}", extra={"tool_name": "health_check"})
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# MCP tools (wrapped versions)
@mcp.tool()
def ping():
    """Simple ping that returns pong with timestamp."""
    return _ping()


@mcp.tool()
def whoami():
    """Get system and user information including APP_ENV."""
    return _whoami()


@mcp.tool()
def time_now(request: TimeRequest) -> Dict[str, Any]:
    """
    Get current time in specified timezone.

    Returns ISO datetime format as requested.
    Includes input validation for timezone parameter.
    """
    return _time_now(request.tz)


@mcp.tool()
def health_check():
    """Returns version, git SHA, and uptime."""
    return _health_check()


def main():
    """Start the MCP server."""
    logger.info(f"Starting {settings.server_name}")
    logger.info("Tools registered: ping, whoami, time_now, health_check")

    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
