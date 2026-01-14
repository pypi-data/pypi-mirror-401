"""
Custom exceptions for the Graph Analyzer package.
"""


class GraphAnalyzerError(Exception):
    """Base exception for all Graph Analyzer errors."""

    pass


class InvalidImageError(GraphAnalyzerError):
    """Raised when the provided image is invalid or cannot be processed."""

    pass


class NoGraphDetectedError(GraphAnalyzerError):
    """Raised when no graph structure is detected in the image."""

    pass


class GraphValidationError(GraphAnalyzerError):
    """Raised when graph validation fails."""

    pass
