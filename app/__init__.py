"""FastMCP server with basic tools."""

import logging
import os
import platform
import socket
import time
from datetime import datetime, timezone, timedelta 
from typing import Dict, Any

from fastmcp import FastMCP
from pydantic import BaseModel, field_validator

from app.config import settings


# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(name=settings.server_name)

# Track server start time  
START_TIME = time.time()


# Input validation for time_now tool
class TimeRequest(BaseModel):
    """Input validation model for time_now tool."""
    tz: str
    
    @field_validator('tz')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone parameter."""
        # Supported timezones
        valid_timezones = ['UTC', 'GMT', 'EST', 'PST', 'IST', 'CET']
        
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
    logger.info("Ping tool called")
    return {
        "message": "pong",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success"
    }


def _whoami():
    """Internal whoami function."""
    logger.info("Whoami tool called")
    try:
        result = {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "username": os.getenv("USER") or os.getenv("USERNAME", "unknown"),
            "app_env": settings.app_env,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success"
        }

        return result
    
    except Exception as e:
        logger.error(f"Whoami failed: {e}")
        return {
            "error": str(e),
            "status": "failed"
        }


def _time_now(tz: str) -> Dict[str, Any]:
    """Internal time_now function with pure logic."""
    logger.info(f"Time_now called for timezone: {tz}")
    
    try:
        # Timezone offset mapping (hours from UTC)
        timezone_offsets = {
            'UTC': 0,
            'GMT': 0,
            'EST': -5,   # Eastern Standard Time
            'PST': -8,   # Pacific Standard Time
            'IST': 5.5,  # India Standard Time (UTC+5:30)
            'CET': 1,    # Central European Time
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
            "status": "success"
        }
        
        logger.info(f"Time calculated successfully for {tz}")
        return result
        
    except Exception as e:
        error_msg = f"Failed to calculate time for {tz}: {str(e)}"
        logger.error(error_msg)
        
        # Consistent error message shape
        return {
            "error": error_msg,
            "status": "failed",
            "timezone": tz
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


def main():
    """Start the MCP server."""
    logger.info(f"Starting {settings.server_name}")
    logger.info("Tools registered: ping, whoami, time_now") 
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
