#!/usr/bin/env python
"""Logging configuration for RINEX parser.

Sets up a configured logger instance for use throughout the RINEX parser module.
"""

import logging

# Create logger
logger = logging.getLogger("rinexparser")
logger.setLevel(logging.INFO)

# Create console handler and set level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Add formatter to handler
ch.setFormatter(formatter)

# Add handler to logger
logger.addHandler(ch)
