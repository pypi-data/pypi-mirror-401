# Graph Analyzer

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/graph-analyzer.svg)](https://badge.fury.io/py/graph-analyzer)

A Python package for analyzing hand-drawn graphs from images. Perfect for students and educators working with graph theory!

## Features

- **Image Analysis**: Analyze hand-drawn or photographed graphs from any device
- **Graph Detection**: Automatically detect nodes and edges using computer vision
- **Simple Graph Validation**: Determine if a graph is a simple graph (no loops, no multiple edges)
- **High Accuracy**: Multiple detection strategies for robust graph recognition
- **Detailed Reports**: Get comprehensive analysis including graph properties
- **Error Handling**: Robust error handling for invalid images and edge cases
- **Easy to Use**: Simple API for quick integration

## What is a Simple Graph?

In graph theory, a **simple graph** is an undirected graph with:
- No self-loops (edges from a vertex to itself)
- No multiple edges between the same pair of vertices

This package helps you verify if your hand-drawn graph meets these criteria!

## Installation

```bash
pip install graph-analyzer
```

### From Source

```bash
git clone https://github.com/mujadid2001/graph-analyzer.git
cd graph-analyzer
pip install -e .
```

### For Development

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from graph_analyzer import GraphAnalyzer

# Initialize the analyzer
analyzer = GraphAnalyzer()

# Analyze an image
result = analyzer.analyze_image('path/to/your/graph_image.jpg')

# Check if it's a simple graph
if result['is_simple_graph']:
    print("✓ This is a simple graph!")
    print(f"Nodes: {result['num_nodes']}")
    print(f"Edges: {result['num_edges']}")
else:
    print("✗ This is NOT a simple graph")
    print("Issues found:")
    for issue in result['issues']:
        print(f"  - {issue}")
```

### Advanced Usage

```python
from graph_analyzer import GraphAnalyzer
import numpy as np

# Initialize with custom settings
analyzer = GraphAnalyzer(
    min_confidence=0.8,  # Higher confidence threshold
    debug_mode=True       # Enable detailed logging
)

# Analyze from different sources
# 1. From file path
result1 = analyzer.analyze_image('graph.jpg')

# 2. From numpy array
image_array = np.array(...)  # Your image as numpy array
result2 = analyzer.analyze_image(image_array)

# 3. Get detailed information
result = analyzer.analyze_image('graph.jpg', return_details=True)
print(f"Detection confidence: {result['confidence']:.2f}")
print(f"Graph properties: {result['graph_properties']}")

# 4. Visualize the detection
vis_image = analyzer.visualize_detection(
    'graph.jpg',
    output_path='output_visualization.jpg'
)
```

### Error Handling

```python
from graph_analyzer import (
    GraphAnalyzer,
    InvalidImageError,
    NoGraphDetectedError,
    GraphValidationError
)

analyzer = GraphAnalyzer()

try:
    result = analyzer.analyze_image('my_graph.jpg')
except InvalidImageError as e:
    print(f"Invalid image: {e}")
except NoGraphDetectedError as e:
    print(f"No graph detected: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## API Reference

### GraphAnalyzer

Main class for analyzing graphs from images.

#### `__init__(min_confidence=0.7, debug_mode=False)`

Initialize the analyzer.

- **min_confidence** (float): Minimum confidence threshold (0-1). Default: 0.7
- **debug_mode** (bool): Enable debug logging. Default: False

#### `analyze_image(image_source, return_details=True)`

Analyze an image to detect and validate a graph structure.

**Parameters:**
- **image_source** (str | Path | np.ndarray): Image file path or numpy array
- **return_details** (bool): Include detailed analysis. Default: True

**Returns:** Dictionary with:
- `is_simple_graph` (bool): Whether it's a simple graph
- `confidence` (float): Detection confidence (0-1)
- `num_nodes` (int): Number of detected nodes
- `num_edges` (int): Number of detected edges
- `issues` (List[str]): List of problems found
- `graph_properties` (Dict): Additional properties (if return_details=True)

#### `visualize_detection(image_source, output_path=None)`

Visualize detected graph structure.

**Parameters:**
- **image_source** (str | Path | np.ndarray): Image file path or numpy array
- **output_path** (str | Path, optional): Save location for visualization

**Returns:** Numpy array with visualization

### Exceptions

- **GraphAnalyzerError**: Base exception for all errors
- **InvalidImageError**: Invalid or corrupted image file
- **NoGraphDetectedError**: No graph structure found in image
- **GraphValidationError**: Graph validation failed

## Examples

### Example 1: Batch Processing

```python
from graph_analyzer import GraphAnalyzer
from pathlib import Path

analyzer = GraphAnalyzer()

# Process multiple images
image_folder = Path('graph_images')
for image_path in image_folder.glob('*.jpg'):
    try:
        result = analyzer.analyze_image(str(image_path))
        print(f"{image_path.name}: Simple graph = {result['is_simple_graph']}")
    except Exception as e:
        print(f"{image_path.name}: Error - {e}")
```

### Example 2: Classroom Usage

```python
from graph_analyzer import GraphAnalyzer

# Grade student submissions
analyzer = GraphAnalyzer(min_confidence=0.75)

student_submissions = {
    'student1.jpg': 'Alice',
    'student2.jpg': 'Bob',
    'student3.jpg': 'Charlie',
}

results = {}
for image_file, student_name in student_submissions.items():
    try:
        result = analyzer.analyze_image(image_file)
        results[student_name] = {
            'correct': result['is_simple_graph'],
            'details': result
        }
    except NoGraphDetectedError:
        results[student_name] = {'correct': False, 'reason': 'No graph detected'}

# Generate report
for student, result in results.items():
    print(f"{student}: {'✓' if result.get('correct') else '✗'}")
```

## How It Works

1. **Image Preprocessing**: The image is converted to grayscale and cleaned up using adaptive thresholding and morphological operations.

2. **Node Detection**: Uses multiple strategies:
   - Hough Circle Transform for circular nodes
   - Contour detection for blob-like structures
   - Filtering based on size and shape

3. **Edge Detection**: Employs:
   - Hough Line Transform for straight edges
   - Connectivity analysis between detected nodes
   - Path validation in the binary image

4. **Graph Validation**: Checks for:
   - Self-loops (edges from a node to itself)
   - Multiple edges between the same nodes
   - Graph connectivity
   - Degree distribution

## Requirements

- Python 3.8+
- numpy >= 1.21.0
- opencv-python >= 4.5.0
- Pillow >= 8.0.0

## Best Practices for Image Capture

For best results when capturing hand-drawn graphs:

1. **Good lighting**: Ensure the image is well-lit
2. **Clear contrast**: Use dark pen/pencil on white paper
3. **Stable camera**: Avoid blurry images
4. **Straight angle**: Capture from directly above
5. **Full graph visible**: Ensure the entire graph is in frame
6. **Clear nodes**: Draw nodes as distinct circles
7. **Clean edges**: Draw edges as clear lines

## Limitations

- Works best with clearly drawn graphs on plain backgrounds
- Node detection assumes roughly circular or blob-like nodes
- Edge detection works best with relatively straight lines
- Very dense or overlapping graphs may have reduced accuracy

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete development setup instructions.

Quick start:

```bash
# Clone and setup
git clone https://github.com/mujadid2001/graph-analyzer.git
cd graph-analyzer
pip install -e ".[dev]"

# Run tests
pytest

# Check code quality
flake8 graph_analyzer/
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=graph_analyzer --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research or educational materials, please cite:

```bibtex
@software{graph_analyzer,
  title = {Graph Analyzer: A Python Package for Analyzing Hand-Drawn Graphs},
  author = {Graph Theory Tools},
  year = {2026},
  url = {https://github.com/mujadid2001/graph-analyzer}
}
```

## Support

- Email: mujadid2001@gmail.com
- GitHub: https://github.com/mujadid2001/graph-analyzer
- Issue Tracker: https://github.com/mujadid2001/graph-analyzer/issues

## Acknowledgments

- Built with OpenCV for computer vision
- Inspired by the needs of graph theory students and educators
- Thanks to all contributors and users

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Latest: v0.1.2** - Repository cleanup and professional organization

---

Made with ❤️ for graph theory students
