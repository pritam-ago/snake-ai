# API Reference

Complete code documentation for the Snake AI project.

## Table of Contents

- [Constants](#constants)
- [Data Classes](#data-classes)
- [SnakeGame Class](#snakegame-class)
  - [Initialization](#initialization)
  - [Game State Methods](#game-state-methods)
  - [Pathfinding Algorithms](#pathfinding-algorithms)
  - [AI Decision Making](#ai-decision-making)
  - [Benchmarking](#benchmarking)
  - [Rendering](#rendering)
- [Main Function](#main-function)

## Constants

### Display Configuration

```python
CELL_SIZE = 25          # Size of each grid cell in pixels
GRID_WIDTH = 24         # Number of cells horizontally
GRID_HEIGHT = 24        # Number of cells vertically
WIDTH = CELL_SIZE * GRID_WIDTH        # Total window width (600px)
HEIGHT = CELL_SIZE * GRID_HEIGHT + 90 # Total window height with panel (690px)
FPS = 12               # Frames per second (game speed)
```

### Benchmark Settings

```python
BENCHMARK_RUNS = 5      # Number of runs per algorithm in benchmark mode
```

### Color Scheme

```python
BG = (18, 18, 18)           # Background color (dark gray)
GRID = (35, 35, 35)         # Grid line color
SNAKE_HEAD = (80, 220, 120) # Snake head color (bright green)
SNAKE_BODY = (40, 170, 90)  # Snake body color (green)
FOOD = (240, 80, 80)        # Food color (red)
TEXT = (240, 240, 240)      # Main text color (white)
SUBTEXT = (180, 180, 180)   # Secondary text color (gray)
PANEL = (28, 28, 28)        # Info panel background
PATH_COLOR = (80, 130, 255) # AI path visualization (blue)
DANGER = (255, 170, 60)     # Warning/highlight color (orange)
```

### Direction Mappings

```python
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

OPPOSITE = {
    "UP": "DOWN",
    "DOWN": "UP",
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
}
```

## Data Classes

### Metrics

Tracks performance metrics during gameplay.

```python
@dataclass
class Metrics:
    algorithm: str = "human"        # Current algorithm name
    nodes_expanded: int = 0         # Nodes explored in last search
    last_path_length: int = 0       # Length of current path
    foods_collected: int = 0        # Total food items eaten
    score: int = 0                  # Current score
    steps_survived: int = 0         # Total steps taken
    computation_ms: float = 0.0     # Last decision time (ms)
    total_decision_ms: float = 0.0  # Cumulative decision time
    decisions_made: int = 0         # Number of AI decisions
    max_snake_length: int = 3       # Longest snake achieved
```

**Usage:**
```python
metrics = Metrics(algorithm="astar")
metrics.score += 1
metrics.steps_survived += 1
```

### BenchmarkResult

Stores results from a single benchmark run.

```python
@dataclass
class BenchmarkResult:
    algorithm: str              # Algorithm name (bfs, dfs, greedy, astar)
    run_number: int            # Run identifier (1-N)
    score: int                 # Final score achieved
    steps_survived: int        # Total steps before game over
    foods_collected: int       # Food items eaten
    avg_nodes_expanded: float  # Average nodes per decision
    avg_decision_ms: float     # Average decision time (ms)
    max_snake_length: int      # Maximum snake length reached
```

**Usage:**
```python
result = BenchmarkResult(
    algorithm="astar",
    run_number=1,
    score=75,
    steps_survived=1500,
    foods_collected=75,
    avg_nodes_expanded=42.5,
    avg_decision_ms=0.065,
    max_snake_length=78
)
```

## SnakeGame Class

Main game class managing state, AI, and rendering.

### Initialization

#### `__init__(self)`

Creates a new game instance.

```python
def __init__(self):
    self.benchmark_results = []         # List of BenchmarkResult objects
    self.benchmark_summary = []         # Summary statistics
    self.show_benchmark_overlay = False # Toggle for results display
    self.reset("human")                 # Start in human mode
```

#### `reset(self, mode="human")`

Resets game to initial state.

**Parameters:**
- `mode` (str): Control mode - "human", "bfs", "dfs", "greedy", or "astar"

**Attributes Set:**
```python
self.snake          # List of (x, y) positions, head first
self.direction      # Current direction: "UP", "DOWN", "LEFT", "RIGHT"
self.next_direction # Next direction to move
self.food          # (x, y) position of food
self.game_over     # Boolean game state
self.mode          # Current control mode
self.metrics       # Metrics instance
self.cached_path   # Current AI path (for visualization)
self.last_reason   # Reason for game over or fallback
```

**Example:**
```python
game = SnakeGame()
game.reset("astar")  # Start A* mode
```

### Game State Methods

#### `spawn_food(self) -> tuple[int, int]`

Spawns food at random unoccupied position.

**Returns:**
- `tuple[int, int]`: (x, y) coordinates of food

**Example:**
```python
food_pos = game.spawn_food()  # e.g., (15, 8)
```

#### `in_bounds(self, pos: tuple[int, int]) -> bool`

Checks if position is within grid boundaries.

**Parameters:**
- `pos`: (x, y) coordinates to check

**Returns:**
- `bool`: True if position is valid, False otherwise

**Example:**
```python
if game.in_bounds((10, 10)):  # True
    print("Valid position")
if game.in_bounds((25, 10)):  # False (out of bounds)
    print("Invalid position")
```

#### `is_occupied(self, pos: tuple[int, int], snake_body=None) -> bool`

Checks if position is occupied by snake.

**Parameters:**
- `pos`: (x, y) coordinates to check
- `snake_body` (optional): Snake body to check against (defaults to `self.snake`)

**Returns:**
- `bool`: True if occupied, False otherwise

**Example:**
```python
if game.is_occupied((5, 5)):
    print("Snake is here")
```

#### `neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]`

Gets all valid neighbor positions (4-directional).

**Parameters:**
- `pos`: (x, y) coordinates

**Returns:**
- `list`: List of valid neighboring positions

**Example:**
```python
neighbors = game.neighbors((10, 10))
# Returns up to 4 neighbors: [(10,9), (10,11), (9,10), (11,10)]
```

#### `safe_neighbors(self, pos: tuple[int, int], blocked: set) -> list[tuple[int, int]]`

Gets neighbors that are not blocked.

**Parameters:**
- `pos`: (x, y) coordinates
- `blocked`: Set of blocked positions

**Returns:**
- `list`: List of safe neighboring positions

**Example:**
```python
blocked = set(game.snake[:-1])  # Snake body except tail
safe = game.safe_neighbors(game.snake[0], blocked)
```

#### `manhattan(self, a: tuple[int, int], b: tuple[int, int]) -> int`

Calculates Manhattan distance between two points.

**Parameters:**
- `a`: First (x, y) position
- `b`: Second (x, y) position

**Returns:**
- `int`: Manhattan distance

**Example:**
```python
dist = game.manhattan((0, 0), (3, 4))  # Returns 7
```

#### `reconstruct_path(self, came_from: dict, start: tuple, goal: tuple) -> list[tuple[int, int]]`

Reconstructs path from search algorithm's came_from dictionary.

**Parameters:**
- `came_from`: Dictionary mapping position -> previous position
- `start`: Starting position
- `goal`: Goal position

**Returns:**
- `list`: Path from start to goal (inclusive)

**Example:**
```python
came_from = {(1,0): (0,0), (2,0): (1,0)}
path = game.reconstruct_path(came_from, (0,0), (2,0))
# Returns [(0,0), (1,0), (2,0)]
```

### Pathfinding Algorithms

All pathfinding methods return `(path, nodes_expanded)` tuple.

#### `bfs(self, start: tuple, goal: tuple, blocked: set) -> tuple[list, int]`

Breadth-First Search implementation.

**Parameters:**
- `start`: Starting (x, y) position
- `goal`: Target (x, y) position
- `blocked`: Set of blocked positions

**Returns:**
- `tuple`: (path_list, nodes_expanded_count)
  - `path_list`: List of positions from start to goal, empty if no path
  - `nodes_expanded_count`: Number of nodes explored

**Time Complexity:** O(b^d) where b=branching factor, d=depth  
**Space Complexity:** O(b^d)  
**Optimal:** Yes  
**Complete:** Yes

**Example:**
```python
path, nodes = game.bfs(
    start=game.snake[0],
    goal=game.food,
    blocked=set(game.snake[:-1])
)
print(f"Found path with {len(path)} steps, explored {nodes} nodes")
```

#### `dfs(self, start: tuple, goal: tuple, blocked: set) -> tuple[list, int]`

Depth-First Search implementation.

**Parameters:**
- Same as BFS

**Returns:**
- Same as BFS

**Time Complexity:** O(b^m) where m=maximum depth  
**Space Complexity:** O(bm)  
**Optimal:** No  
**Complete:** Yes (with cycle detection)

#### `greedy(self, start: tuple, goal: tuple, blocked: set) -> tuple[list, int]`

Greedy Best-First Search using Manhattan distance heuristic.

**Parameters:**
- Same as BFS

**Returns:**
- Same as BFS

**Time Complexity:** O(b^d) worst case  
**Space Complexity:** O(b^d)  
**Optimal:** No  
**Complete:** No

#### `astar(self, start: tuple, goal: tuple, blocked: set) -> tuple[list, int]`

A* Search implementation.

**Parameters:**
- Same as BFS

**Returns:**
- Same as BFS

**Time Complexity:** O(b^d)  
**Space Complexity:** O(b^d)  
**Optimal:** Yes (with admissible heuristic)  
**Complete:** Yes

**Example:**
```python
path, nodes = game.astar(
    start=(10, 10),
    goal=(15, 15),
    blocked={(11, 10), (12, 10)}
)
```

### AI Decision Making

#### `flood_fill_space(self, start: tuple, blocked: set) -> int`

Counts available space from a position using flood fill.

**Parameters:**
- `start`: Starting position
- `blocked`: Set of blocked positions

**Returns:**
- `int`: Number of reachable cells

**Purpose:** Used by fallback system to avoid trapping the snake.

**Example:**
```python
space = game.flood_fill_space((10, 10), set(game.snake))
print(f"{space} cells accessible")
```

#### `choose_fallback_move(self) -> str | None`

Chooses safest move when no direct path to food exists.

**Returns:**
- `str`: Direction name ("UP", "DOWN", "LEFT", "RIGHT") or None if no safe move

**Algorithm:**
1. For each possible direction:
   - Skip if opposite to current direction
   - Skip if out of bounds or hits body
   - Calculate available space using flood fill
   - Calculate distance to food
2. Rank by: most space > closest to food
3. Return best direction

**Example:**
```python
direction = game.choose_fallback_move()
if direction:
    game.next_direction = direction
```

#### `get_ai_move(self) -> str`

Main AI decision-making function. Runs search algorithm and chooses move.

**Returns:**
- `str`: Direction to move

**Process:**
1. Run appropriate search algorithm
2. Update metrics (nodes expanded, computation time, etc.)
3. If path found, extract next move
4. Otherwise, use fallback system
5. If no safe move, continue current direction

**Side Effects:**
- Updates `self.metrics`
- Updates `self.cached_path`
- Updates `self.last_reason`

**Example:**
```python
if game.mode != "human":
    next_move = game.get_ai_move()
    game.next_direction = next_move
```

### Game Loop

#### `step(self)`

Executes one game step (move snake, check collisions, update score).

**Process:**
1. Get AI move if not in human mode
2. Update direction (prevent 180° turns)
3. Calculate new head position
4. Check wall collision
5. Check self-collision
6. Move snake
7. Check food collection
8. Update metrics

**Side Effects:**
- Modifies `self.snake`
- May set `self.game_over = True`
- Updates `self.metrics`
- May spawn new food

**Example:**
```python
while not game.game_over:
    game.step()
    game.draw()
    clock.tick(FPS)
```

### Benchmarking

#### `run_single_algorithm_game(self, mode: str, seed=None, max_steps=1500) -> BenchmarkResult`

Runs one complete game for benchmarking.

**Parameters:**
- `mode`: Algorithm to test ("bfs", "dfs", "greedy", "astar")
- `seed` (optional): Random seed for reproducibility
- `max_steps`: Maximum steps before ending (default 1500)

**Returns:**
- `BenchmarkResult`: Performance data from the run

**Example:**
```python
result = game.run_single_algorithm_game("astar", seed=42, max_steps=1000)
print(f"Score: {result.score}, Steps: {result.steps_survived}")
```

#### `run_benchmark(self, runs_per_algorithm=BENCHMARK_RUNS)`

Runs full benchmark suite across all algorithms.

**Parameters:**
- `runs_per_algorithm`: Number of runs per algorithm (default 5)

**Process:**
1. For each algorithm (bfs, dfs, greedy, astar):
   - Run N games with different seeds
   - Collect results
2. Calculate summary statistics
3. Export to CSV
4. Show results overlay

**Side Effects:**
- Updates `self.benchmark_results`
- Updates `self.benchmark_summary`
- Creates `snake_ai_benchmark_results.csv`
- Sets `self.show_benchmark_overlay = True`

**Example:**
```python
game.run_benchmark(runs_per_algorithm=10)
```

#### `export_benchmark_csv(self)`

Exports benchmark results to CSV file.

**Output File:** `snake_ai_benchmark_results.csv`

**CSV Columns:**
- algorithm
- run_number
- score
- steps_survived
- foods_collected
- avg_nodes_expanded
- avg_decision_ms
- max_snake_length

**Example:**
```python
game.export_benchmark_csv()
# Creates/overwrites snake_ai_benchmark_results.csv
```

### Input Handling

#### `handle_key(self, key: int)`

Processes keyboard input.

**Parameters:**
- `key`: Pygame key constant (e.g., `pygame.K_UP`)

**Key Mappings:**
- `K_UP/DOWN/LEFT/RIGHT`: Set direction (human mode)
- `K_h`: Switch to human mode
- `K_1`: Switch to BFS
- `K_2`: Switch to DFS
- `K_3`: Switch to Greedy
- `K_4`: Switch to A*
- `K_r`: Restart current mode
- `K_b`: Run benchmark
- `K_TAB`: Toggle benchmark overlay

**Example:**
```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        game.handle_key(event.key)
```

### Rendering

#### `draw_grid(self)`

Draws grid lines on the game screen.

#### `draw_path(self)`

Draws AI's planned path in blue (if in AI mode).

#### `draw_benchmark_overlay(self)`

Draws benchmark results overlay when enabled.

#### `draw(self)`

Main rendering function. Draws entire game state.

**Process:**
1. Fill background
2. Draw grid
3. Draw AI path (if applicable)
4. Draw food
5. Draw snake
6. Draw info panel
7. Draw game over overlay (if game over)
8. Draw benchmark overlay (if enabled)
9. Flip display

**Example:**
```python
game.draw()
pygame.display.flip()
```

## Main Function

#### `main()`

Application entry point. Runs the game loop.

**Process:**
1. Create SnakeGame instance
2. Event loop:
   - Handle quit events
   - Handle keyboard input
3. Game loop:
   - Step game state
   - Render frame
   - Control FPS

**Example:**
```python
if __name__ == "__main__":
    main()
```

## Usage Examples

### Creating a Custom Game Mode

```python
game = SnakeGame()
game.reset("astar")

while not game.game_over:
    game.step()
    game.draw()
    
    # Custom logic
    if game.metrics.score >= 50:
        print("High score achieved!")
        break
    
    clock.tick(FPS)
```

### Running Batch Benchmarks

```python
game = SnakeGame()

results = []
for algo in ["bfs", "dfs", "greedy", "astar"]:
    for run in range(10):
        result = game.run_single_algorithm_game(algo, seed=run)
        results.append(result)
        print(f"{algo} run {run+1}: score={result.score}")
```

### Custom Pathfinding

```python
def custom_search(game, start, goal, blocked):
    # Your algorithm here
    path = [start, goal]  # Simplified
    nodes_expanded = 10
    return path, nodes_expanded

# Use it
game = SnakeGame()
path, nodes = custom_search(game, game.snake[0], game.food, set(game.snake))
```

## Type Hints

For better IDE support, consider adding type hints:

```python
from typing import List, Tuple, Set, Dict, Optional

Position = Tuple[int, int]
Path = List[Position]
Direction = str  # "UP", "DOWN", "LEFT", "RIGHT"
```

## Error Handling

The code includes minimal error handling. Consider adding:

```python
def safe_step(game: SnakeGame) -> bool:
    """Step with error handling."""
    try:
        game.step()
        return True
    except Exception as e:
        print(f"Error during step: {e}")
        return False
```

## Performance Optimization

For better performance:

1. **Use sets for lookups:**
   ```python
   blocked = set(self.snake[:-1])  # O(1) lookup
   ```

2. **Cache flood fill results:**
   ```python
   self.flood_fill_cache = {}
   ```

3. **Limit benchmark runs:**
   ```python
   BENCHMARK_RUNS = 3  # Faster testing
   ```

## References

- [Algorithm Guide](algorithms.md) - Detailed algorithm explanations
- [Benchmarking Guide](benchmarking.md) - Performance testing
- [Configuration](configuration.md) - Customization options
