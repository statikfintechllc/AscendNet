"""
AscendNet Unified Logging System
"""

import logging
import os
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup unified logging for AscendNet"""
    
    # Create logs directory
    log_dir = Path(os.environ.get('HOME', '/home/user')) / "AscendNet" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger("AscendNet")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / "ascendnet.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Set up specific loggers for components
    setup_component_loggers()
    
    return logger

def setup_component_loggers():
    """Setup specific loggers for different components"""
    
    components = [
        "AscendNet.API",
        "AscendNet.P2P", 
        "AscendNet.Compute",
        "AscendNet.Storage",
        "AscendNet.Payments",
        "AscendNet.GremlinGPT",
        "AscendNet.GodCore",
        "AscendNet.SignalCore"
    ]
    
    for component in components:
        logger = logging.getLogger(component)
        logger.setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific component"""
    return logging.getLogger(f"AscendNet.{name}")
