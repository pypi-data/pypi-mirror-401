"""Centralized logging configuration using Rich."""

import logging
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

# Define custom theme for agents
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "agent.planning": "blue",
    "agent.coding": "green",
    "agent.execution": "magenta",
    "agent.task": "white",
    "agent.error": "red",
})

console = Console(theme=custom_theme)

def setup_logging(level: str = "INFO"):
    """
    Configure structured logging with Rich.
    
    Args:
        level: Logging level (default: INFO)
    """
    # Create logger
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(
            console=console,
            rich_tracebacks=True,
            show_path=False,
            markup=True
        )]
    )
    
    # Suppress noisy 3rd party loggers
    loggers_to_silence = [
        "httpx", "httpcore", "openai", "urllib3", "asyncio", 
        "multipart", "starlette", "watchfiles", "aiosqlite"
    ]
    for logger_name in loggers_to_silence:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    logging.getLogger("uvicorn").setLevel(logging.INFO) # Keep uvicorn info
    logging.getLogger("uvicorn.access").setLevel(logging.ERROR) # Suppress access logs completely for cleaner output

    logging.info("📝 Logging initialized with Rich")

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)
