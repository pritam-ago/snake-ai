# Snake AI Documentation

Welcome to the Snake AI project documentation. This project implements and compares different search algorithms in the classic Snake game environment.

## Quick Links

- **[Quick Reference](quick-reference.md)** - ⚡ Fast lookup for common tasks and controls
- [Getting Started](getting-started.md) - Installation and first steps
- [Algorithm Guide](algorithms.md) - Detailed explanation of each search algorithm
- [API Reference](api-reference.md) - Code structure and class documentation
- [Benchmarking Guide](benchmarking.md) - How to run and interpret benchmarks
- [Configuration](configuration.md) - Customization options
- [Contributing](contributing.md) - How to contribute to the project

## Overview

This project demonstrates how different pathfinding algorithms perform in a dynamic environment where the goal (food) changes and the obstacles (snake body) grow over time.

### Implemented Algorithms

1. **Breadth-First Search (BFS)** - Guarantees shortest path
2. **Depth-First Search (DFS)** - Explores depth-first
3. **Greedy Best-First Search** - Heuristic-based approach
4. **A* Search** - Optimal pathfinding algorithm

### Key Features

- Real-time visualization of algorithm decisions
- Performance metrics tracking
- Automated benchmarking system
- CSV export for data analysis
- Fallback safety system to prevent self-trapping

## Project Structure

```
snake-ai/
├── snake_ai_working_model.py      # Main game implementation
├── snake_ai_benchmark_results.csv # Benchmark results (generated)
├── README.md                      # Project overview
└── docs/                          # Documentation folder
    ├── index.md                   # This file
    ├── getting-started.md         # Installation and setup
    ├── algorithms.md              # Algorithm explanations
    ├── api-reference.md           # Code documentation
    ├── benchmarking.md            # Benchmarking guide
    ├── configuration.md           # Configuration options
    └── contributing.md            # Contribution guidelines
```

## Quick Start

```bash
# Install dependencies
pip install pygame

# Run the game
python snake_ai_working_model.py

# Press '4' to watch A* algorithm play
# Press 'B' to run benchmarks
```

## Use Cases

This project is useful for:

- **Learning**: Understanding how search algorithms work in practice
- **Teaching**: Demonstrating algorithm performance differences
- **Research**: Comparing pathfinding strategies in dynamic environments
- **Game Development**: Implementing AI for grid-based games

## Support

For issues, questions, or contributions, please refer to:
- [Main README](../README.md) for project overview
- [Contributing Guide](contributing.md) for development guidelines

## License

This project is open source and available for educational purposes.
