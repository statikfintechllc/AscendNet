#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Centralized Logging Configuration

import os
import sys
from pathlib import Path
from loguru import logger

# Base logging directory - use project directory instead of home
project_root = Path(__file__).parent.parent
BASE_LOG_DIR = project_root / "data" / "logs"


def setup_module_logger(module_name, log_level="INFO"):
    """
    Setup dedicated logger for a specific module

    Args:
        module_name (str): Name of the module (e.g., 'backend', 'nlp_engine', 'scraper')
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logger: Configured logger instance
    """
    # Ensure log directory exists
    module_log_dir = BASE_LOG_DIR / module_name
    module_log_dir.mkdir(parents=True, exist_ok=True)

    # Set proper permissions
    os.chmod(str(module_log_dir), 0o755)

    # Configure module-specific log file
    log_file = module_log_dir / f"{module_name}.log"

    # Remove existing handlers for this module to avoid duplicates
    logger.remove()

    # Add module-specific file handler
    logger.add(
        str(log_file),
        rotation="10 MB",
        retention="30 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )

    # Add console handler for development
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Set file permissions
    if log_file.exists():
        os.chmod(str(log_file), 0o644)

    logger.info(f"[LOGGING] Module logger initialized for {module_name} -> {log_file}")
    return logger


def get_module_logger(module_name, log_level="INFO"):
    """
    Get or create a logger for a specific module

    Args:
        module_name (str): Name of the module
        log_level (str): Logging level

    Returns:
        logger: Configured logger instance
    """
    return setup_module_logger(module_name, log_level)


def create_all_module_loggers():
    """
    Create loggers for all major system modules
    """
    modules = [
        "backend",
        "nlp_engine",
        "memory",
        "scraper",
        "agents",
        "trading_core",
        "tools",
        "core",
        "executors",
        "self_training",
        "self_mutation_watcher",
        "utils",
        "tests",
        "frontend",
    ]

    for module in modules:
        setup_module_logger(module)

    logger.success(f"[LOGGING] Initialized loggers for {len(modules)} modules")


if __name__ == "__main__":
    create_all_module_loggers()
