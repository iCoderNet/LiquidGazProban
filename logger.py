"""
Logging Configuration for LiquidGazProban
Provides structured logging throughout the application
"""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from config import LogConfig

def setup_logger(name: Optional[str] = None, log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup and configure application logger
    
    Args:
        name: Logger name (defaults to root logger)
        log_file: Path to log file (defaults to config)
    
    Returns:
        Configured logger instance
    """
    # Get logger
    logger = logging.getLogger(name or __name__)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set log level
    log_level = getattr(logging, LogConfig.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        LogConfig.LOG_FORMAT,
        datefmt=LogConfig.LOG_DATE_FORMAT
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    log_path = log_file or LogConfig.LOG_FILE
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=LogConfig.MAX_LOG_SIZE,
        backupCount=LogConfig.BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create default logger
default_logger = setup_logger('LiquidGazProban')

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f'LiquidGazProban.{name}')
    return default_logger

# Convenience functions
def log_info(message: str, logger_name: Optional[str] = None):
    """Log info message"""
    get_logger(logger_name).info(message)

def log_error(message: str, logger_name: Optional[str] = None, exc_info: bool = False):
    """Log error message"""
    get_logger(logger_name).error(message, exc_info=exc_info)

def log_warning(message: str, logger_name: Optional[str] = None):
    """Log warning message"""
    get_logger(logger_name).warning(message)

def log_debug(message: str, logger_name: Optional[str] = None):
    """Log debug message"""
    get_logger(logger_name).debug(message)

if __name__ == "__main__":
    # Test logging
    test_logger = get_logger('Test')
    test_logger.info("✅ Logger initialized successfully")
    test_logger.debug("Debug message")
    test_logger.warning("Warning message")
    test_logger.error("Error message")
