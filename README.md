# Snake AI - Search Algorithms Comparison

A Python-based Snake game implementation featuring multiple AI search algorithms with real-time visualization and performance benchmarking. This project demonstrates how different pathfinding algorithms (BFS, DFS, Greedy Best-First Search, and A*) perform in the classic Snake game environment.

## Documentation

📚 **[Complete Documentation Overview](DOCUMENTATION.md)** - Full guide to all documentation (3,400+ lines)

For comprehensive documentation, see the [docs](docs/) folder:

- **[Quick Reference](docs/quick-reference.md)** - ⚡ Fast lookup for controls and common tasks
- **[Getting Started](docs/getting-started.md)** - Installation, setup, and first steps
- **[Algorithm Guide](docs/algorithms.md)** - Detailed explanation of each search algorithm
- **[API Reference](docs/api-reference.md)** - Complete code documentation
- **[Benchmarking Guide](docs/benchmarking.md)** - Performance testing and analysis
- **[Configuration](docs/configuration.md)** - Customization options
- **[Contributing](docs/contributing.md)** - How to contribute to the project

## Features

- **Multiple Play Modes**
  - Human-controlled gameplay
  - AI-controlled with 4 different search algorithms

- **Search Algorithms Implemented**
  - **BFS (Breadth-First Search)**: Guarantees shortest path, explores level by level
  - **DFS (Depth-First Search)**: Explores as far as possible along each branch
  - **Greedy Best-First Search**: Uses heuristics to move closer to the goal
  - **A* Search**: Optimal pathfinding combining actual and heuristic costs

- **Real-time Visualization**
  - Visual path highlighting showing AI decision-making
  - Metrics display (score, steps, path length, nodes expanded, computation time)
  - Clean grid-based UI with color-coded elements

- **Benchmarking System**
  - Automated testing across all algorithms
  - Performance metrics comparison
  - CSV export for further analysis
  - Statistical summaries (averages, best runs)

- **Safety Features**
  - Fallback move selection when no path to food exists
  - Flood-fill space calculation to avoid trapping the snake
  - Collision detection and boundary checking

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. Clone or download this repository
2. Install the required dependency:

```bash
pip install pygame
```

## Usage

### Running the Game

```bash
python snake_ai_working_model.py
```

### Controls

| Key | Action |
|-----|--------|
| H | Switch to Human mode |
| 1 | Switch to BFS algorithm |
| 2 | Switch to DFS algorithm |
| 3 | Switch to Greedy Best-First Search |
| 4 | Switch to A* Search |
| B | Run automated benchmark (all algorithms) |
| TAB | Show/hide benchmark results overlay |
| R | Restart current mode |
| ESC | Quit game |
| Arrow Keys | Control snake (Human mode only) |

## Configuration

You can modify these constants in the code to customize the game:

```python
CELL_SIZE = 25          # Size of each grid cell in pixels
GRID_WIDTH = 24         # Number of cells horizontally
GRID_HEIGHT = 24        # Number of cells vertically
FPS = 12               # Game speed (frames per second)
BENCHMARK_RUNS = 5     # Number of runs per algorithm in benchmark
```

## Benchmarking

Press **B** to run an automated benchmark that:
1. Tests all 4 AI algorithms
2. Runs each algorithm 5 times (configurable)
3. Collects performance metrics
4. Exports results to `snake_ai_benchmark_results.csv`
5. Displays summary overlay in-game

### Benchmark Metrics

- **Average Score**: Mean food items collected
- **Average Steps**: Mean survival steps
- **Average Foods**: Mean food items eaten
- **Average Nodes**: Mean nodes expanded per decision
- **Average ms**: Mean computation time per decision
- **Best Score**: Highest score achieved in any run
- **Max Snake Length**: Longest snake achieved

## Algorithm Comparison

Based on benchmark results, here's a typical performance comparison:

| Algorithm | Avg Score | Avg Steps | Best Score | Avg Decision Time |
|-----------|-----------|-----------|------------|-------------------|
| BFS | ~75 | ~1357 | ~84 | ~0.13 ms |
| DFS | ~0.4 | ~1500 | ~1 | ~0.29 ms |
| Greedy | ~79 | ~1462 | ~83 | ~0.03 ms |
| A* | ~81 | ~1500 | ~84 | ~0.06 ms |

**Observations:**
- **A*** typically performs best with optimal pathfinding
- **Greedy** is fastest but slightly less optimal
- **BFS** is reliable but slower than A* and Greedy
- **DFS** struggles significantly in this domain due to its exploratory nature

## Project Structure

```
snake-ai/
├── snake_ai_working_model.py      # Main game file with all algorithms
├── snake_ai_benchmark_results.csv # Benchmark output (generated)
└── README.md                      # This file
```

## How It Works

### Pathfinding
Each AI algorithm searches for a path from the snake's head to the food while avoiding the snake's body. When a direct path isn't available, a fallback system chooses the move with the most open space.

### Safety System
The fallback move selection uses flood-fill to calculate available space in each direction, preventing the snake from trapping itself.

### Metrics Collection
The game tracks:
- Nodes expanded during pathfinding
- Computation time per decision
- Path length
- Score and survival steps
- Maximum snake length achieved

## Technical Details

- Built with **Pygame** for graphics and game loop
- Uses standard Python data structures (deque, heapq) for efficient algorithm implementation
- Real-time performance monitoring with microsecond precision
- CSV export using Python's csv module for data analysis

For detailed technical documentation, see the [API Reference](docs/api-reference.md).

## Future Enhancements

Potential improvements:
- Additional algorithms (Dijkstra's, Jump Point Search)
- Hamiltonian cycle strategy
- Neural network-based AI
- Multi-food scenarios
- Obstacle variations
- Performance optimizations for larger grids

See [Contributing Guide](docs/contributing.md) for how to help implement these features.

## Project Structure

```
snake-ai/
├── snake_ai_working_model.py      # Main game implementation
├── snake_ai_benchmark_results.csv # Benchmark output (generated)
├── README.md                      # This file
└── docs/                          # Documentation
    ├── index.md                   # Documentation home
    ├── getting-started.md         # Setup guide
    ├── algorithms.md              # Algorithm details
    ├── api-reference.md           # Code documentation
    ├── benchmarking.md            # Benchmark guide
    ├── configuration.md           # Configuration options
    └── contributing.md            # Contribution guidelines
```

## License

This project is open source and available for educational purposes.

## Acknowledgments

Inspired by classic Snake games and search algorithm visualizations. Built as a demonstration of AI search algorithms in a practical gaming context.
