"""
Main analyzer module for detecting and validating graphs from images.
"""

import cv2
import numpy as np
from typing import Dict, Optional, Union
from pathlib import Path
import logging

from .exceptions import InvalidImageError, NoGraphDetectedError
from .graph_detector import GraphDetector
from .graph_validator import GraphValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphAnalyzer:
    """
    Main class for analyzing hand-drawn graphs from images.

    This class provides functionality to:
    - Load and preprocess images
    - Detect graph structures (nodes and edges)
    - Validate if the detected structure is a simple graph
    - Provide detailed analysis results

    Attributes:
        min_confidence (float): Minimum confidence (0-1)
        debug_mode (bool): Enable debug visualization
    """

    def __init__(self, min_confidence: float = 0.7,
                 debug_mode: bool = False):
        """
        Initialize the GraphAnalyzer.

        Args:
            min_confidence: Minimum confidence threshold (0-1)
            debug_mode: Enable debug mode for logging/visualization

        Raises:
            ValueError: If min_confidence is not between 0 and 1
        """
        if not 0 <= min_confidence <= 1:
            raise ValueError("min_confidence must be between 0 and 1")

        self.min_confidence = min_confidence
        self.debug_mode = debug_mode
        self.detector = GraphDetector(debug_mode=debug_mode)
        self.validator = GraphValidator()

        if debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.debug("GraphAnalyzer initialized in debug mode")

    def analyze_image(
        self, image_source: Union[str, Path, np.ndarray],
        return_details: bool = True
    ) -> Dict:
        """
        Analyze an image to detect and validate a graph structure.

        Args:
            image_source: Path to image file, Path, or numpy array
            return_details: If True, return detailed analysis info

        Returns:
            Dictionary containing:
                - is_simple_graph (bool): If structure is simple
                - confidence (float): Detection confidence score
                - num_nodes (int): Number of detected nodes
                - num_edges (int): Number of detected edges
                - issues (List[str]): Issues (if not simple)
                - graph_properties (Dict): Additional properties

        Raises:
            InvalidImageError: If the image cannot be loaded or is invalid
            NoGraphDetectedError: If no graph structure is detected
        """
        # Load and validate image
        image = self._load_image(image_source)

        # Detect graph structure
        logger.info("Detecting graph structure...")
        detection_result = self.detector.detect_graph(image)

        if not detection_result["graph_detected"]:
            raise NoGraphDetectedError(
                "No graph structure detected in the image. "
                "Please ensure the image contains a clear hand-drawn graph."
            )

        # Validate if it's a simple graph
        logger.info("Validating graph properties...")
        validation_result = self.validator.validate_simple_graph(
            nodes=detection_result["nodes"], edges=detection_result["edges"]
        )

        # Compile results
        result = {
            "is_simple_graph": validation_result["is_simple"],
            "confidence": detection_result["confidence"],
            "num_nodes": len(detection_result["nodes"]),
            "num_edges": len(detection_result["edges"]),
            "issues": validation_result["issues"],
        }

        if return_details:
            result.update(
                {
                    "graph_properties": {
                        "has_loops": validation_result["has_loops"],
                        "has_multiple_edges": (
                            validation_result["has_multiple_edges"]
                        ),
                        "is_connected": (
                            validation_result.get("is_connected", None)
                        ),
                        "max_degree": (
                            validation_result.get("max_degree", None)
                        ),
                    },
                    "nodes": detection_result["nodes"],
                    "edges": detection_result["edges"],
                    "detection_method": (
                        detection_result.get("method", "hybrid")
                    ),
                }
            )

        simple = result['is_simple_graph']
        logger.info(f"Analysis complete: Simple graph = {simple}")
        return result

    def _load_image(self, image_source: Union[str, Path, np.ndarray]
                    ) -> np.ndarray:
        """
        Load and validate an image from various sources.

        Args:
            image_source: Path to image file, Path object, or numpy array

        Returns:
            Numpy array containing the image

        Raises:
            InvalidImageError: If the image cannot be loaded or is invalid
        """
        if isinstance(image_source, np.ndarray):
            image = image_source
        else:
            # Convert to Path object for consistent handling
            image_path = Path(image_source)

            if not image_path.exists():
                raise InvalidImageError(f"Image file not found: {image_path}")

            # Read image
            image = cv2.imread(str(image_path))

            if image is None:
                raise InvalidImageError(
                    f"Failed to load image from {image_path}. "
                    "Please ensure the file is a valid image format."
                )

        # Validate image
        if image.size == 0:
            raise InvalidImageError("Image is empty")

        if len(image.shape) < 2:
            raise InvalidImageError("Invalid image dimensions")

        logger.debug(f"Image loaded successfully: shape={image.shape}")
        return image

    def visualize_detection(
        self,
        image_source: Union[str, Path, np.ndarray],
        output_path: Optional[Union[str, Path]] = None,
    ) -> np.ndarray:
        """
        Visualize the detected graph structure on the original image.

        Args:
            image_source: Path to image file, Path object, or numpy array
            output_path: Optional path to save the visualization

        Returns:
            Numpy array containing the visualization

        Raises:
            InvalidImageError: If the image cannot be loaded
            NoGraphDetectedError: If no graph is detected
        """
        image = self._load_image(image_source)
        detection_result = self.detector.detect_graph(image)

        if not detection_result["graph_detected"]:
            raise NoGraphDetectedError("No graph detected for visualization")

        # Create visualization
        vis_image = image.copy()

        # Draw edges
        for edge in detection_result["edges"]:
            pt1 = tuple(map(int, edge["start"]))
            pt2 = tuple(map(int, edge["end"]))
            cv2.line(vis_image, pt1, pt2, (0, 255, 0), 2)

        # Draw nodes
        for node in detection_result["nodes"]:
            center = tuple(map(int, node["position"]))
            cv2.circle(vis_image, center, 10, (255, 0, 0), -1)
            cv2.circle(vis_image, center, 12, (0, 0, 255), 2)

        # Save if output path is provided
        if output_path:
            cv2.imwrite(str(output_path), vis_image)
            logger.info(f"Visualization saved to {output_path}")

        return vis_image
