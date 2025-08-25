import logging
from datetime import datetime, timezone
from app.config import settings

# Custom formatter for structured logging
class StructuredFormatter(logging.Formatter):
    
    def format(self, record):
        log_parts = [
            f"timestamp={datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}Z",
            f"level={record.levelname}",
            f"component=mcp_server",
            f"function={record.funcName}",
            f"message={record.getMessage()}"
        ]
        
        # Add extra fields if present
        if hasattr(record, 'tool_name'):
            log_parts.insert(-1, f"tool={record.tool_name}")
        if hasattr(record, 'execution_time'):
            log_parts.append(f"execution_time_ms={record.execution_time:.2f}")
            
        return " ".join(log_parts)

# Setup logger
logger = logging.getLogger("mcp_server")
logger.setLevel(getattr(logging, settings.log_level))

# Clear any existing handlers
logger.handlers.clear()

# Create formatter
formatter = StructuredFormatter()

# Console handler (for terminal output)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler (writes to docs/logs.txt)
file_handler = logging.FileHandler('docs/logs.txt', mode='a')  # 'a' append each time
file_handler.setFormatter(formatter)

# Add both handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent duplicate logs
logger.propagate = False


