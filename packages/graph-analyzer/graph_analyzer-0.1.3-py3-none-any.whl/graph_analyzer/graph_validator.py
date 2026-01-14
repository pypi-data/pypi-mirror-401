"""
Graph validation module for checking graph properties.
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class GraphValidator:
    """
    Validates graph properties and determines if a graph is simple.

    A simple graph is defined as:
    - Undirected graph
    - No loops (edges from a vertex to itself)
    - No multiple edges between the same pair of vertices
    """

    def __init__(self):
        """Initialize the GraphValidator."""
        pass

    def validate_simple_graph(self, nodes: List[Dict],
                              edges: List[Dict]) -> Dict:
        """
        Validate if the detected graph structure is a simple graph.

        Args:
            nodes: List of detected nodes
            edges: List of detected edges

        Returns:
            Dictionary containing:
                - is_simple (bool): If the graph is simple
                - has_loops (bool): If self-loops exist
                - has_multiple_edges (bool): If multiple edges exist
                - issues (List[str]): List of issues found
                - is_connected (bool): If graph is connected
                - max_degree (int): Maximum degree of any vertex
        """
        issues = []
        has_loops = False
        has_multiple_edges = False

        # Check for self-loops
        for edge in edges:
            if edge["start_node"] == edge["end_node"]:
                has_loops = True
                msg = f"Self-loop detected at node {edge['start_node']}"
                issues.append(msg)

        # Check for multiple edges
        edge_set = set()
        for edge in edges:
            # Create a normalized edge representation (undirected)
            edge_key = tuple(sorted([edge["start_node"], edge["end_node"]]))

            if edge_key in edge_set:
                has_multiple_edges = True
                issues.append(
                    f"Multiple edges detected between nodes "
                    f"{edge['start_node']} and {edge['end_node']}"
                )
            else:
                edge_set.add(edge_key)

        # Check connectivity
        is_connected = self._is_connected(nodes, edges)
        if not is_connected and len(nodes) > 1:
            issues.append("Graph is not connected (has isolated components)")

        # Calculate max degree
        max_degree = self._calculate_max_degree(nodes, edges)

        # Determine if it's a simple graph
        is_simple = not has_loops and not has_multiple_edges

        if is_simple:
            logger.info("Graph is a valid simple graph")
        else:
            logger.warning(f"Graph is not simple. Issues: {issues}")

        return {
            "is_simple": is_simple,
            "has_loops": has_loops,
            "has_multiple_edges": has_multiple_edges,
            "issues": issues,
            "is_connected": is_connected,
            "max_degree": max_degree,
        }

    def _is_connected(self, nodes: List[Dict], edges: List[Dict]) -> bool:
        """
        Check if the graph is connected using BFS.

        Args:
            nodes: List of nodes
            edges: List of edges

        Returns:
            True if graph is connected
        """
        if len(nodes) == 0:
            return True

        if len(nodes) == 1:
            return True

        # Build adjacency list
        adjacency = {node["id"]: [] for node in nodes}
        for edge in edges:
            adjacency[edge["start_node"]].append(edge["end_node"])
            adjacency[edge["end_node"]].append(edge["start_node"])

        # BFS from first node
        visited = set()
        queue = [nodes[0]["id"]]
        visited.add(nodes[0]["id"])

        while queue:
            current = queue.pop(0)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Graph is connected if all nodes are visited
        return len(visited) == len(nodes)

    def _calculate_max_degree(self, nodes: List[Dict],
                              edges: List[Dict]) -> int:
        """
        Calculate the maximum degree of any vertex.

        Args:
            nodes: List of nodes
            edges: List of edges

        Returns:
            Maximum degree
        """
        if len(nodes) == 0:
            return 0

        # Count degree for each node
        degree = {node["id"]: 0 for node in nodes}

        for edge in edges:
            degree[edge["start_node"]] += 1
            degree[edge["end_node"]] += 1

        return max(degree.values()) if degree else 0

    def get_graph_properties(self, nodes: List[Dict],
                             edges: List[Dict]) -> Dict:
        """
        Get additional graph properties.

        Args:
            nodes: List of nodes
            edges: List of edges

        Returns:
            Dictionary of graph properties
        """
        num_nodes = len(nodes)
        num_edges = len(edges)

        properties = {
            "num_vertices": num_nodes,
            "num_edges": num_edges,
            "density": 0.0,
            "is_tree": False,
            "is_complete": False,
        }

        if num_nodes > 1:
            # Calculate graph density
            max_edges = num_nodes * (num_nodes - 1) // 2
            if max_edges > 0:
                properties["density"] = num_edges / max_edges
            else:
                properties["density"] = 0

            # Check if it's a tree (connected and n-1 edges)
            is_connected = self._is_connected(nodes, edges)
            properties["is_tree"] = is_connected and num_edges == num_nodes - 1

            # Check if it's complete (all possible edges exist)
            properties["is_complete"] = num_edges == max_edges

        return properties
