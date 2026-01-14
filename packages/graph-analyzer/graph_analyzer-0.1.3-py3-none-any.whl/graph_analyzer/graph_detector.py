"""
Graph detection module using computer vision techniques.
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class GraphDetector:
    """
    Detect graph structures from images using computer vision.

    This class implements multiple detection strategies:
    - Circle detection (Hough Circles) for nodes
    - Line detection (Hough Lines) for edges
    - Contour-based detection for nodes
    - Connected components analysis
    """

    def __init__(self, debug_mode: bool = False):
        """
        Initialize the GraphDetector.

        Args:
            debug_mode: Enable debug mode for additional logging
        """
        self.debug_mode = debug_mode

    def detect_graph(self, image: np.ndarray) -> Dict:
        """
        Detect graph structure from an image.

        Args:
            image: Input image as numpy array

        Returns:
            Dictionary containing:
                - graph_detected (bool): Whether a graph was detected
                - nodes (List[Dict]): List of detected nodes
                - edges (List[Dict]): List of detected edges
                - confidence (float): Detection confidence score
                - method (str): Detection method used
        """
        # Preprocess image
        preprocessed = self._preprocess_image(image)

        # Try multiple detection strategies
        nodes = self._detect_nodes(preprocessed, image)

        if len(nodes) == 0:
            logger.warning("No nodes detected in image")
            return {
                "graph_detected": False,
                "nodes": [],
                "edges": [],
                "confidence": 0.0,
                "method": "none",
            }

        edges = self._detect_edges(preprocessed, nodes, image)

        # Calculate confidence based on detection quality
        confidence = self._calculate_confidence(nodes, edges, image.shape)

        return {
            "graph_detected": True,
            "nodes": nodes,
            "edges": edges,
            "confidence": confidence,
            "method": "hybrid",
        }

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better detection.

        Args:
            image: Input image

        Returns:
            Preprocessed grayscale image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive thresholding for better edge detection
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        logger.debug("Image preprocessing complete")
        return cleaned

    def _detect_nodes(self, preprocessed: np.ndarray,
                      original: np.ndarray) -> List[Dict]:
        """
        Detect graph nodes using multiple strategies.

        Args:
            preprocessed: Preprocessed binary image
            original: Original image

        Returns:
            List of detected nodes with positions
        """
        nodes = []

        # Strategy 1: Detect circles using Hough Circle Transform
        if len(original.shape) == 3:
            gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        else:
            gray = original
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=25,
            param1=50,
            param2=25,
            minRadius=8,
            maxRadius=60,
        )

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                nodes.append(
                    {
                        "id": len(nodes),
                        "position": (int(circle[0]), int(circle[1])),
                        "radius": int(circle[2]),
                        "detection_method": "hough_circle",
                    }
                )

        # Strategy 2: Detect blobs using contour detection
        contours, _ = cv2.findContours(
            preprocessed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            area = cv2.contourArea(contour)
            # Filter by area to detect node-sized objects
            if 50 < area < 2000:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Check if this position is not too close to existing nodes
                    is_new = True
                    for existing_node in nodes:
                        dist = np.sqrt(
                            (cx - existing_node["position"][0]) ** 2
                            + (cy - existing_node["position"][1]) ** 2
                        )
                        if dist < 25:
                            is_new = False
                            break

                    if is_new:
                        nodes.append(
                            {
                                "id": len(nodes),
                                "position": (cx, cy),
                                "radius": int(np.sqrt(area / np.pi)),
                                "detection_method": "contour",
                            }
                        )

        logger.debug(f"Detected {len(nodes)} nodes")
        return nodes

    def _detect_edges(
        self, preprocessed: np.ndarray, nodes: List[Dict], original: np.ndarray
    ) -> List[Dict]:
        """
        Detect edges between nodes.

        Args:
            preprocessed: Preprocessed binary image
            nodes: List of detected nodes
            original: Original image

        Returns:
            List of detected edges
        """
        edges = []

        # Create a mask without nodes to detect edges better
        mask = preprocessed.copy()
        for node in nodes:
            cv2.circle(mask, node["position"], node["radius"] + 5, 0, -1)

        # Detect lines using Hough Line Transform
        lines = cv2.HoughLinesP(
            mask, rho=1, theta=np.pi / 180, threshold=50,
            minLineLength=20, maxLineGap=10
        )

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]

                # Find closest nodes to line endpoints
                start_node = self._find_closest_node((x1, y1), nodes)
                end_node = self._find_closest_node((x2, y2), nodes)

                if start_node is not None and end_node is not None:
                    # Check if edge already exists
                    edge_exists = False
                    for existing_edge in edges:
                        if (
                            existing_edge["start_node"] == start_node["id"]
                            and existing_edge["end_node"] == end_node["id"]
                        ) or (
                            existing_edge["start_node"] == end_node["id"]
                            and existing_edge["end_node"] == start_node["id"]
                        ):
                            edge_exists = True
                            break

                    if not edge_exists and start_node["id"] != end_node["id"]:
                        edges.append(
                            {
                                "start": start_node["position"],
                                "end": end_node["position"],
                                "start_node": start_node["id"],
                                "end_node": end_node["id"],
                                "detection_method": "hough_line",
                            }
                        )

        # Check connectivity between nearby nodes
        for i, node1 in enumerate(nodes):
            nodes_after = nodes[i + 1:]
            for j, node2 in enumerate(nodes_after, start=i + 1):
                dist = np.sqrt(
                    (node1["position"][0] - node2["position"][0]) ** 2
                    + (node1["position"][1] - node2["position"][1]) ** 2
                )

                # If nodes are reasonably close, check for connection
                if 30 < dist < 200:
                    if self._check_connection(node1, node2, preprocessed):
                        # Check if edge already exists
                        edge_exists = False
                        for existing_edge in edges:
                            if (
                                existing_edge["start_node"] == node1["id"]
                                and existing_edge["end_node"] == node2["id"]
                            ) or (
                                existing_edge["start_node"] == node2["id"]
                                and existing_edge["end_node"] == node1["id"]
                            ):
                                edge_exists = True
                                break

                        if not edge_exists:
                            edges.append(
                                {
                                    "start": node1["position"],
                                    "end": node2["position"],
                                    "start_node": node1["id"],
                                    "end_node": node2["id"],
                                    "detection_method": "connectivity",
                                }
                            )

        logger.debug(f"Detected {len(edges)} edges")
        return edges

    def _find_closest_node(
        self, point: Tuple[int, int], nodes: List[Dict],
        max_distance: float = 40.0
    ) -> Dict:
        """
        Find the closest node to a given point.

        Args:
            point: (x, y) coordinates
            nodes: List of nodes
            max_distance: Maximum distance to consider

        Returns:
            Closest node or None
        """
        min_dist = float("inf")
        closest_node = None

        for node in nodes:
            dist = np.sqrt(
                (point[0] - node["position"][0]) ** 2 +
                (point[1] - node["position"][1]) ** 2
            )
            if dist < min_dist and dist < max_distance:
                min_dist = dist
                closest_node = node

        return closest_node

    def _check_connection(self, node1: Dict, node2: Dict,
                          preprocessed: np.ndarray) -> bool:
        """
        Check if there's a visual connection between two nodes.

        Args:
            node1: First node
            node2: Second node
            preprocessed: Preprocessed binary image

        Returns:
            True if connection exists
        """
        # Sample points along the line between nodes
        x1, y1 = node1["position"]
        x2, y2 = node2["position"]

        num_samples = 10
        white_pixels = 0

        for i in range(1, num_samples):
            t = i / num_samples
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))

            if (0 <= y < preprocessed.shape[0] and
                    0 <= x < preprocessed.shape[1]):
                if preprocessed[y, x] > 0:
                    white_pixels += 1

        # If more than 40% of samples are white, consider it connected
        return white_pixels / (num_samples - 1) > 0.4

    def _calculate_confidence(
        self, nodes: List[Dict], edges: List[Dict], image_shape: Tuple
    ) -> float:
        """
        Calculate confidence score for the detection.

        Args:
            nodes: Detected nodes
            edges: Detected edges
            image_shape: Shape of the image

        Returns:
            Confidence score between 0 and 1
        """
        if len(nodes) == 0:
            return 0.0

        # Base confidence on number of nodes and edges
        node_score = min(len(nodes) / 10.0, 1.0) * 0.4
        edge_score = min(len(edges) / 15.0, 1.0) * 0.3

        # Consider graph connectivity
        avg_degree = (2 * len(edges)) / len(nodes) if len(nodes) > 0 else 0
        degree_score = min(avg_degree / 4.0, 1.0) * 0.3

        confidence = node_score + edge_score + degree_score

        return min(confidence, 1.0)
