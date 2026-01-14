# Quick Start Guide - Graph Analyzer

## Installation

```bash
pip install graph-analyzer
```

## Your First Analysis

### 1. Create a simple test script

Create a file called `test_graph.py`:

```python
from graph_analyzer import GraphAnalyzer

# Initialize the analyzer
analyzer = GraphAnalyzer()

# Analyze your graph image
result = analyzer.analyze_image('my_graph.jpg')

# Print results
print(f"Is it a simple graph? {result['is_simple_graph']}")
print(f"Number of nodes: {result['num_nodes']}")
print(f"Number of edges: {result['num_edges']}")
print(f"Confidence: {result['confidence']:.1%}")

if not result['is_simple_graph']:
    print("\nIssues found:")
    for issue in result['issues']:
        print(f"  - {issue}")
```

### 2. Run it

```bash
python test_graph.py
```

## Generate Test Images

Don't have a graph image? Generate test images:

```python
from examples.generate_test_images import main
main()
```

This creates:
- `test_simple_graph.jpg` - A valid simple graph
- `test_non_simple_graph.jpg` - A graph with a self-loop

## Tips for Best Results

### Drawing Your Graph

1. **Use dark pen/pencil on white paper**
2. **Draw clear circles for nodes**
3. **Draw straight lines for edges**
4. **Ensure good lighting when photographing**
5. **Capture from directly above**

### Example: Good Graph
```
    O--------O
    |\      /|
    | \    / |
    |  \  /  |
    |   \/   |
    |   /\   |
    |  /  \  |
    | /    \ |
    |/      \|
    O--------O
```

### Adjusting Sensitivity

```python
# More strict detection
analyzer = GraphAnalyzer(min_confidence=0.8)

# More lenient detection
analyzer = GraphAnalyzer(min_confidence=0.6)

# Enable debug output
analyzer = GraphAnalyzer(debug_mode=True)
```

## Common Use Cases

### 1. Homework Checker

```python
from graph_analyzer import GraphAnalyzer

analyzer = GraphAnalyzer()

homework_files = [
    'problem1.jpg',
    'problem2.jpg',
    'problem3.jpg'
]

for i, file in enumerate(homework_files, 1):
    try:
        result = analyzer.analyze_image(file)
        status = "✓" if result['is_simple_graph'] else "✗"
        print(f"Problem {i}: {status}")
    except Exception as e:
        print(f"Problem {i}: Error - {e}")
```

### 2. Batch Processing

```python
from pathlib import Path
from graph_analyzer import GraphAnalyzer

analyzer = GraphAnalyzer()
results = {}

for image_path in Path('graphs/').glob('*.jpg'):
    try:
        result = analyzer.analyze_image(str(image_path))
        results[image_path.name] = result['is_simple_graph']
    except Exception as e:
        results[image_path.name] = f"Error: {e}"

# Print summary
simple_count = sum(1 for v in results.values() if v is True)
print(f"Simple graphs: {simple_count}/{len(results)}")
```

### 3. Interactive Analysis

```python
from graph_analyzer import GraphAnalyzer

analyzer = GraphAnalyzer(debug_mode=True)

while True:
    image_path = input("Enter image path (or 'quit'): ")
    if image_path.lower() == 'quit':
        break
    
    try:
        result = analyzer.analyze_image(image_path)
        
        if result['is_simple_graph']:
            print("✓ This IS a simple graph!")
        else:
            print("✗ This is NOT a simple graph")
            print("Reasons:")
            for issue in result['issues']:
                print(f"  - {issue}")
        
        # Save visualization
        vis_path = image_path.replace('.jpg', '_result.jpg')
        analyzer.visualize_detection(image_path, vis_path)
        print(f"Visualization saved to: {vis_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print()
```

## Understanding Results

### Result Dictionary

```python
result = {
    'is_simple_graph': True,          # Main result
    'confidence': 0.85,                # Detection confidence (0-1)
    'num_nodes': 5,                    # Number of nodes detected
    'num_edges': 7,                    # Number of edges detected
    'issues': [],                      # List of problems (empty if simple)
    'graph_properties': {              # Additional properties
        'has_loops': False,            # Self-loops present?
        'has_multiple_edges': False,   # Multiple edges present?
        'is_connected': True,          # Is graph connected?
        'max_degree': 4                # Maximum node degree
    }
}
```

### What Makes a Simple Graph?

A **simple graph** must have:
- ✓ No self-loops (edge from a node to itself)
- ✓ No multiple edges (more than one edge between same nodes)
- ✓ Undirected edges only

## Error Handling

```python
from graph_analyzer import (
    GraphAnalyzer,
    InvalidImageError,
    NoGraphDetectedError
)

analyzer = GraphAnalyzer()

try:
    result = analyzer.analyze_image('my_graph.jpg')
    
except InvalidImageError:
    print("The image file is invalid or corrupted")
    
except NoGraphDetectedError:
    print("No graph structure found in the image")
    print("Tips:")
    print("  - Ensure the image is clear")
    print("  - Check that nodes are visible")
    print("  - Verify edges are drawn")
    
except FileNotFoundError:
    print("Image file not found")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Next Steps

- Check out the [full README](README.md) for more details
- Explore [example scripts](examples/) for advanced usage
- Read the [API documentation](README.md#api-reference)
- Contribute to the project (see [CONTRIBUTING.md](CONTRIBUTING.md))

## Need Help?

- 📧 Email: mujadid2001@gmail.com
- 🔗 GitHub: https://github.com/mujadid2001/graph-analyzer
- 🐛 Report issues: https://github.com/mujadid2001/graph-analyzer/issues

Happy graph analyzing! 🎉
