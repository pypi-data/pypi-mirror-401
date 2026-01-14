"""
Graph Analyzer - A Python package for analyzing hand-drawn graphs from images.

This package helps students and researchers analyze graph theory problems by
detecting and validating graphs from hand-drawn or photographed images.
"""

__version__ = "0.1.3"
__author__ = "Hafiz Muhammad Mujadid Majeed"
__email__ = "mujadid2001@gmail.com"

from .analyzer import GraphAnalyzer
from .exceptions import (
    GraphAnalyzerError,
    InvalidImageError,
    NoGraphDetectedError,
    GraphValidationError,
)

__all__ = [
    "GraphAnalyzer",
    "GraphAnalyzerError",
    "InvalidImageError",
    "NoGraphDetectedError",
    "GraphValidationError",
]
