"""
Logging utilities for vc_web_email.

This module provides a configured logger for email operations.
"""

import logging
import sys
from typing import Optional


class EmailLogger:
    """
    Logging utility for email operations.
    
    Provides a configured logger with optional debug mode.
    """
    
    _logger: Optional[logging.Logger] = None
    _debug_mode: bool = False
    
    @classmethod
    def get_logger(cls, name: str = 'vc_web_email', debug: bool = False) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name
            debug: Enable debug mode
        
        Returns:
            Configured logger instance
        """
        if cls._logger is None or cls._debug_mode != debug:
            cls._logger = cls._create_logger(name, debug)
            cls._debug_mode = debug
        
        return cls._logger
    
    @classmethod
    def _create_logger(cls, name: str, debug: bool) -> logging.Logger:
        """Create and configure a new logger."""
        logger = logging.getLogger(name)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Set level based on debug mode
        level = logging.DEBUG if debug else logging.INFO
        logger.setLevel(level)
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        
        # Create formatter
        if debug:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    @classmethod
    def debug(cls, message: str, *args, **kwargs) -> None:
        """Log a debug message."""
        cls.get_logger(debug=cls._debug_mode).debug(message, *args, **kwargs)
    
    @classmethod
    def info(cls, message: str, *args, **kwargs) -> None:
        """Log an info message."""
        cls.get_logger(debug=cls._debug_mode).info(message, *args, **kwargs)
    
    @classmethod
    def warning(cls, message: str, *args, **kwargs) -> None:
        """Log a warning message."""
        cls.get_logger(debug=cls._debug_mode).warning(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message: str, *args, **kwargs) -> None:
        """Log an error message."""
        cls.get_logger(debug=cls._debug_mode).error(message, *args, **kwargs)
    
    @classmethod
    def exception(cls, message: str, *args, **kwargs) -> None:
        """Log an exception with traceback."""
        cls.get_logger(debug=cls._debug_mode).exception(message, *args, **kwargs)
    
    @classmethod
    def set_debug(cls, debug: bool) -> None:
        """Enable or disable debug mode."""
        cls._debug_mode = debug
        cls._logger = cls._create_logger('vc_web_email', debug)
