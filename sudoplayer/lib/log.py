from datetime import datetime
from loguru import logger

date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logger.add(
    f"logs/sudoplayer-{date}.log",  # Log file path
    rotation="10 MB",  # Rotate log file when it reaches 10 MB
    retention="30 days",  # Keep logs for 30 days
    level="DEBUG",  # Log level
    format="{time} {level} {message}",  # Log format
)

logger = logger.bind(
    name="Sudoplayer"
)  # Bind a name to the logger for better identification
