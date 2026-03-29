# Quick Reference Guide

Quick reference for the Snake AI project.

## Installation

```bash
pip install pygame
python snake_ai_working_model.py
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| **H** | Human mode |
| **1** | BFS algorithm |
| **2** | DFS algorithm |
| **3** | Greedy Best-First Search |
| **4** | A* Search (Recommended) |
| **B** | Run benchmark (all algorithms) |
| **TAB** | Show/hide benchmark results |
| **R** | Restart current mode |
| **ESC** | Quit |
| **Arrows** | Control snake (Human mode) |

## Algorithm Quick Comparison

| Algorithm | Speed | Quality | When to Use |
|-----------|-------|---------|-------------|
| **A*** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Best overall** - Recommended |
| **Greedy** | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | Need fastest decisions |
| **BFS** | ⚡⚡ | ⭐⭐⭐⭐ | Learning/demonstrations |
| **DFS** | ⚡ | ⭐ | Don't use (poor performance) |

## Common Tasks

### Watch AI Play
```
1. Run: python snake_ai_working_model.py
2. Press 4 (for A*)
3. Watch the snake play itself
```

### Run Performance Tests
```
1. Run: python snake_ai_working_model.py
2. Press B
3. Wait for completion
4. Press TAB to view results
5. Check snake_ai_benchmark_results.csv
```

### Change Game Speed
Edit line 32 in `snake_ai_working_model.py`:
```python
FPS = 12  # Lower = slower, Higher = faster
```

### Change Grid Size
Edit lines 28-29:
```python
GRID_WIDTH = 24   # Horizontal cells
GRID_HEIGHT = 24  # Vertical cells
```

## File Locations

| File | Purpose |
|------|---------|
| `snake_ai_working_model.py` | Main game code |
| `snake_ai_benchmark_results.csv` | Benchmark data (generated) |
| `README.md` | Project overview |
| `docs/` | Full documentation |

## Typical Benchmark Results

| Metric | BFS | DFS | Greedy | A* |
|--------|-----|-----|--------|-----|
| Avg Score | ~75 | ~0.4 | ~79 | **~81** |
| Avg Speed | 0.13ms | 0.29ms | **0.03ms** | 0.06ms |
| Avg Steps | 1357 | 1500 | 1462 | **1500** |

**Winner**: A* (best score, good speed)  
**Fastest**: Greedy (0.03ms decisions)  
**Avoid**: DFS (terrible performance)

## Display Metrics Explained

Bottom panel shows:
```
Mode: ASTAR    Score: 15    Steps: 342
PathLen: 8    Nodes: 12    Time: 0.05 ms
```

- **Mode**: Current algorithm
- **Score**: Food items collected
- **Steps**: Total moves made
- **PathLen**: Length of planned path
- **Nodes**: Cells examined in last search
- **Time**: Decision computation time

## Color Coding

- **Bright Green**: Snake head
- **Green**: Snake body
- **Red**: Food
- **Blue**: AI's planned path
- **Orange**: Warning/highlight text

## Quick Configuration

### Slow Motion (for watching)
```python
FPS = 6
```

### Small Grid (faster games)
```python
GRID_WIDTH = 16
GRID_HEIGHT = 16
```

### Fast Benchmark (quick test)
```python
BENCHMARK_RUNS = 3
max_steps = 1000  # In run_single_algorithm_game
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No module named 'pygame'" | Run: `pip install pygame` |
| Window doesn't open | Use graphical environment (not SSH) |
| Game too fast/slow | Change `FPS` value |
| Benchmark takes forever | Reduce `BENCHMARK_RUNS` to 3 |

## Learning Resources

**Start here:**
1. [Getting Started](getting-started.md) - Setup and basics
2. Run game and try each algorithm (keys 1-4)
3. Read [Algorithm Guide](algorithms.md) - Understand how they work

**Deep dive:**
1. [Benchmarking Guide](benchmarking.md) - Performance analysis
2. [API Reference](api-reference.md) - Code structure
3. [Configuration](configuration.md) - Customization

**Contributing:**
- [Contributing Guide](contributing.md) - Add features or fix bugs

## Code Snippets

### Import and Run
```python
from snake_ai_working_model import SnakeGame

game = SnakeGame()
game.reset("astar")

while not game.game_over:
    game.step()
    # Process game state
```

### Run Single Benchmark
```python
game = SnakeGame()
result = game.run_single_algorithm_game("astar", seed=42)
print(f"Score: {result.score}")
```

### Custom Grid
```python
GRID_WIDTH = 32
GRID_HEIGHT = 32
game = SnakeGame()
```

## Performance Tips

**For faster execution:**
- Increase FPS: `FPS = 30`
- Reduce benchmark runs: `BENCHMARK_RUNS = 3`
- Use Greedy algorithm (fastest decisions)

**For better scores:**
- Use A* algorithm
- Larger grids give more room
- Lower FPS doesn't affect AI quality

## Links

- **Main Documentation**: [docs/index.md](index.md)
- **Full README**: [../README.md](../README.md)
- **Source Code**: `snake_ai_working_model.py`

## Quick Stats

- **Lines of Code**: ~556
- **Algorithms**: 4 (BFS, DFS, Greedy, A*)
- **Grid Size**: 24x24 (576 cells)
- **Max Snake Length**: ~87 (from benchmarks)
- **Average A* Score**: ~81

---

**Need help?** Check the [Getting Started Guide](getting-started.md) or [API Reference](api-reference.md).
