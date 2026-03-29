# Getting Started

This guide will help you set up and run the Snake AI project.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher**
  - Check your version: `python --version`
  - Download from: https://www.python.org/downloads/

- **pip** (Python package manager)
  - Usually comes with Python
  - Check: `pip --version`

## Installation

### Step 1: Get the Project

Clone or download the repository to your local machine:

```bash
# If using git
git clone <repository-url>
cd snake-ai

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies

Install the required Python package:

```bash
pip install pygame
```

**Note**: If you have both Python 2 and 3 installed, you may need to use `pip3` instead:

```bash
pip3 install pygame
```

### Step 3: Verify Installation

Check that pygame is installed correctly:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

This should print the pygame version (e.g., "2.5.2").

## Running the Game

### Basic Execution

Run the main Python file:

```bash
python snake_ai_working_model.py
```

A window will open showing the Snake game in human control mode.

### First Steps

Once the game is running:

1. **Try Human Mode** (default)
   - Use arrow keys to control the snake
   - Try to collect the red food without hitting walls or yourself

2. **Watch AI Play**
   - Press `4` to activate A* algorithm
   - Watch how the AI navigates to the food
   - Observe the blue path showing the AI's planned route

3. **Compare Algorithms**
   - Press `1` for BFS
   - Press `2` for DFS
   - Press `3` for Greedy
   - Press `4` for A*
   - Notice the differences in behavior and performance

4. **Run Benchmarks**
   - Press `B` to run automated benchmarks
   - Wait for all tests to complete
   - View results overlay with `TAB`
   - Check `snake_ai_benchmark_results.csv` for detailed data

## Controls Reference

| Key | Action |
|-----|--------|
| **H** | Switch to Human control mode |
| **1** | Switch to BFS algorithm |
| **2** | Switch to DFS algorithm |
| **3** | Switch to Greedy Best-First Search |
| **4** | Switch to A* Search |
| **B** | Run automated benchmark (all algorithms) |
| **TAB** | Toggle benchmark results overlay |
| **R** | Restart current mode |
| **ESC** | Quit game |
| **Arrow Keys** | Control snake (Human mode only) |

## Understanding the Display

### Game Grid
- **Green cells**: Snake body
- **Bright green cell**: Snake head
- **Red cell**: Food
- **Blue cells**: AI's planned path (AI modes only)

### Information Panel (Bottom)
The bottom panel shows real-time metrics:

```
Mode: ASTAR    Score: 15    Steps: 342
PathLen: 8    Nodes: 12    Time: 0.05 ms
```

- **Mode**: Current control mode (HUMAN, BFS, DFS, GREEDY, ASTAR)
- **Score**: Number of food items collected
- **Steps**: Total moves made
- **PathLen**: Length of current planned path
- **Nodes**: Number of nodes explored in last search
- **Time**: Computation time for last decision (milliseconds)

### Benchmark Overlay
Press `TAB` after running benchmarks to see:

- Average performance across multiple runs
- Comparison between all algorithms
- Best scores achieved
- Decision-making speed

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"

**Solution**: Pygame is not installed. Run:
```bash
pip install pygame
```

### "python: command not found"

**Solution**: Python is not in your PATH. Try:
- Windows: `py snake_ai_working_model.py`
- Linux/Mac: `python3 snake_ai_working_model.py`

### Game window doesn't open

**Solution**: 
- Ensure you're running in a graphical environment (not SSH/remote terminal)
- Update pygame: `pip install --upgrade pygame`
- Check display settings if using WSL or virtual machines

### Game runs too fast/slow

**Solution**: Modify the `FPS` constant in the code (line 32):
```python
FPS = 12  # Lower = slower, Higher = faster
```

### Benchmark takes too long

**Solution**: Reduce the number of runs or max steps:
```python
BENCHMARK_RUNS = 3  # Default is 5 (line 33)
max_steps = 1000    # In run_single_algorithm_game method (line 346)
```

## Next Steps

Now that you have the game running:

1. **Learn about the algorithms** - Read the [Algorithm Guide](algorithms.md)
2. **Run benchmarks** - See the [Benchmarking Guide](benchmarking.md)
3. **Customize settings** - Check the [Configuration Guide](configuration.md)
4. **Explore the code** - Review the [API Reference](api-reference.md)

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.9+, Linux (any modern distribution)
- **Python**: 3.7+
- **RAM**: 256 MB
- **Display**: 800x600 resolution

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 512 MB
- **Display**: 1024x768 or higher

## Additional Resources

- [Main README](../README.md) - Project overview
- [Pygame Documentation](https://www.pygame.org/docs/) - Learn more about pygame
- [Python Documentation](https://docs.python.org/3/) - Python language reference
