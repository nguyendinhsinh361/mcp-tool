"""
Centralized logging configuration for MCP Project.
Provides a LogManager class to handle logger creation and configuration.
"""
import logging
import sys
from typing import Dict, Optional


class LogManager:
    """
    Centralized logging manager for MCP Project.
    Manages logger instances, formatting, and logging levels.
    """
    
    # Default format for log messages
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Class variable to store logger instances
    _loggers: Dict[str, logging.Logger] = {}
    
    def __init__(self, default_level: int = logging.INFO):
        """
        Initialize the logging manager with default settings.
        
        Args:
            default_level: Default logging level to use for new loggers
        """
        self.default_level = default_level
        self.default_format = self.DEFAULT_FORMAT
        
        # Initialize the main application logger
        self.main_logger = self.get_logger("MCP TOOLS")
    
    def get_logger(self, name: str, level: Optional[int] = None) -> logging.Logger:
        """
        Get or create a logger with the specified name and level.
        If a logger with the given name already exists, return that instance.
        
        Args:
            name: The logger name
            level: The logging level (uses default_level if None)
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # If we already have this logger, return it
        if name in self._loggers:
            return self._loggers[name]
        
        # Create a new logger
        logger = self._setup_logger(name, level or self.default_level)
        self._loggers[name] = logger
        
        return logger
    
    def _setup_logger(self, name: str, level: int) -> logging.Logger:
        """
        Internal method to set up a logger with consistent formatting.
        
        Args:
            name: The logger name
            level: The logging level
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Create console handler and set level if no handlers exist
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            
            # Create formatter
            formatter = logging.Formatter(self.default_format)
            
            # Add formatter to handler
            handler.setFormatter(formatter)
            
            # Add handler to logger
            logger.addHandler(handler)
        
        return logger
    
    def set_default_format(self, format_str: str) -> None:
        """
        Set the default format for new loggers.
        
        Args:
            format_str: The format string to use
        """
        self.default_format = format_str
    
    def set_default_level(self, level: int) -> None:
        """
        Set the default logging level for new loggers.
        
        Args:
            level: The logging level to use
        """
        self.default_level = level
    
    def update_all_loggers(self, level: Optional[int] = None, format_str: Optional[str] = None) -> None:
        """
        Update all existing loggers with new level and/or format.
        
        Args:
            level: New logging level (if None, keeps current levels)
            format_str: New format string (if None, keeps current formats)
        """
        if level is None and format_str is None:
            return
            
        for logger_name, logger in self._loggers.items():
            # Update level if specified
            if level is not None:
                logger.setLevel(level)
                for handler in logger.handlers:
                    handler.setLevel(level)
            
            # Update format if specified
            if format_str is not None:
                formatter = logging.Formatter(format_str)
                for handler in logger.handlers:
                    handler.setFormatter(formatter)
    
    def add_file_handler(self, logger_name: str, file_path: str, level: Optional[int] = None) -> None:
        """
        Add a file handler to the specified logger.
        
        Args:
            logger_name: Name of the logger to modify
            file_path: Path to the log file
            level: Logging level for this handler (uses logger's level if None)
        """
        if logger_name not in self._loggers:
            self.get_logger(logger_name)
            
        logger = self._loggers[logger_name]
        
        # Create file handler
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level if level is not None else logger.level)
        
        # Set formatter
        formatter = logging.Formatter(self.default_format)
        file_handler.setFormatter(formatter)
        
        # Add to logger
        logger.addHandler(file_handler)


# Create a global instance of LogManager
log_manager = LogManager()

# Create main application logger
logger = log_manager.main_logger

# Backward compatibility function
def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    Wrapper around log_manager.get_logger for backward compatibility.
    
    Args:
        name: The logger name
        level: The logging level
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return log_manager.get_logger(name, level)
