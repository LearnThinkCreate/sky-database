"""
"""
from .google_sheets import readSpreadsheet, updateSpreadsheet, createSpreadsheet
from .style import BaseStyle, HysonStyle

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())