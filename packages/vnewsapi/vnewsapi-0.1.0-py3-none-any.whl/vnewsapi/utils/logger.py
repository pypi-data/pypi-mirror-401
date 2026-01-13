"""
Logging utilities for vnewsapi.
Adapted from vnstock.
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional


def setup_logger(
    name: str,
    level: str = 'INFO',
    handler_type: str = 'stream',
    filename: Optional[str] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    max_bytes: int = 10485760,
    backup_count: int = 5,
    debug: bool = False
) -> logging.Logger:
    """
    Configure and return a customizable logger.

    Args:
        name (str): The logger's name
        level (str): Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        handler_type (str): Type of handler ('stream', 'file', 'rotating')
        filename (Optional[str]): Path to log file
        log_format (Optional[str]): Format of the log messages
        date_format (Optional[str]): Format of the timestamp
        max_bytes (int): Maximum log file size in bytes (for 'rotating' handler)
        backup_count (int): Number of backup files to keep
        debug (bool): If True, set level to DEBUG

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set level
    if debug:
        level = 'DEBUG'
    
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Set default file name if none provided
    if filename is None and handler_type in ('file', 'rotating'):
        filename = os.path.join(os.getcwd(), f'{name}.log')

    # Set default log format if not provided
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if date_format is None:
        date_format = '%Y-%m-%d %H:%M:%S'

    # Create formatter
    formatter = logging.Formatter(log_format, date_format)

    # Determine the handler type
    if handler_type == 'file' and filename:
        handler = logging.FileHandler(filename)
    elif handler_type == 'rotating' and filename:
        handler = RotatingFileHandler(filename, maxBytes=max_bytes, backupCount=backup_count)
    else:  # Default to stream handler
        handler = logging.StreamHandler()

    # Set formatter and add handler to logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


def get_logger(name: str, level: str = 'INFO', debug: bool = False) -> logging.Logger:
    """
    Get or create a logger with default configuration.

    Args:
        name (str): Logger name
        level (str): Logging level
        debug (bool): If True, set level to DEBUG

    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    
    # Only setup if no handlers exist
    if not logger.handlers:
        if debug:
            level = 'DEBUG'
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # Add console handler if none exists
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

