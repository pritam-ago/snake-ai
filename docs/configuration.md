# Configuration Guide

This guide covers all configuration options and customization possibilities for the Snake AI project.

## Quick Configuration Reference

| Setting | Default | Range | Impact |
|---------|---------|-------|--------|
| CELL_SIZE | 25 | 10-50 | Visual cell size |
| GRID_WIDTH | 24 | 8-50 | Game width |
| GRID_HEIGHT | 24 | 8-50 | Game height |
| FPS | 12 | 1-60 | Game speed |
| BENCHMARK_RUNS | 5 | 1-20 | Benchmark iterations |

## Display Configuration

### Grid Dimensions

Located at: `snake_ai_working_model.py` lines 27-32

```python
CELL_SIZE = 25          # Pixels per grid cell
GRID_WIDTH = 24         # Number of cells horizontally
GRID_HEIGHT = 24        # Number of cells vertically
```

#### Adjusting Grid Size

**Smaller Grid (faster games):**
```python
CELL_SIZE = 20
GRID_WIDTH = 16
GRID_HEIGHT = 16
```

**Larger Grid (longer games):**
```python
CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 32
```

**Effects:**
- Smaller grids = faster games, more challenging
- Larger grids = longer games, more space to maneuver
- Cell size affects visual appearance only

**Recommendations:**
- **Learning/Demo**: 16x16 (quick games)
- **Standard**: 24x24 (balanced)
- **Challenge**: 32x32 or larger (long games)

### Window Size

Automatically calculated:
```python
WIDTH = CELL_SIZE * GRID_WIDTH        # Game area width
HEIGHT = CELL_SIZE * GRID_HEIGHT + 90 # Includes info panel
```

**Info Panel Height**: Fixed at 90 pixels

**To modify panel height:**
```python
PANEL_HEIGHT = 90  # Change this value
HEIGHT = CELL_SIZE * GRID_HEIGHT + PANEL_HEIGHT
```

### Game Speed

```python
FPS = 12  # Frames per second
```

**Speed Options:**
- **Slow** (1-6 FPS): Easy to watch and understand
- **Medium** (7-15 FPS): Standard gameplay
- **Fast** (16-30 FPS): Quick games, harder to follow
- **Very Fast** (31-60 FPS): Rapid benchmarking

**Examples:**
```python
FPS = 6   # Slow motion for demonstrations
FPS = 12  # Default balanced speed
FPS = 20  # Faster gameplay
FPS = 60  # Maximum speed
```

**Note**: FPS does not affect AI decision-making or benchmark metrics.

## Visual Customization

### Color Scheme

Located at: `snake_ai_working_model.py` lines 35-44

```python
BG = (18, 18, 18)           # Background
GRID = (35, 35, 35)         # Grid lines
SNAKE_HEAD = (80, 220, 120) # Snake head
SNAKE_BODY = (40, 170, 90)  # Snake body
FOOD = (240, 80, 80)        # Food
TEXT = (240, 240, 240)      # Main text
SUBTEXT = (180, 180, 180)   # Secondary text
PANEL = (28, 28, 28)        # Info panel
PATH_COLOR = (80, 130, 255) # AI path
DANGER = (255, 170, 60)     # Highlights
```

Colors are RGB tuples: `(red, green, blue)` with values 0-255.

#### Pre-made Color Themes

**Classic Green Theme** (default):
```python
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (40, 170, 90)
FOOD = (240, 80, 80)
```

**Blue Ice Theme**:
```python
BG = (15, 20, 30)
SNAKE_HEAD = (100, 200, 255)
SNAKE_BODY = (50, 120, 200)
FOOD = (255, 100, 100)
PATH_COLOR = (200, 220, 255)
```

**Neon Theme**:
```python
BG = (10, 10, 10)
SNAKE_HEAD = (0, 255, 0)
SNAKE_BODY = (0, 200, 0)
FOOD = (255, 0, 255)
PATH_COLOR = (0, 255, 255)
GRID = (50, 50, 50)
```

**Dark Mode**:
```python
BG = (0, 0, 0)
GRID = (20, 20, 20)
SNAKE_HEAD = (60, 180, 100)
SNAKE_BODY = (30, 130, 70)
FOOD = (200, 50, 50)
TEXT = (220, 220, 220)
PANEL = (15, 15, 15)
```

**High Contrast** (accessibility):
```python
BG = (255, 255, 255)
GRID = (200, 200, 200)
SNAKE_HEAD = (0, 100, 0)
SNAKE_BODY = (0, 150, 0)
FOOD = (200, 0, 0)
TEXT = (0, 0, 0)
SUBTEXT = (80, 80, 80)
PANEL = (240, 240, 240)
PATH_COLOR = (0, 0, 200)
```

### Font Configuration

```python
font = pygame.font.SysFont("consolas", 22)        # Main font
small_font = pygame.font.SysFont("consolas", 16)  # Secondary font
```

**To change fonts:**
```python
# Different font family
font = pygame.font.SysFont("arial", 22)
font = pygame.font.SysFont("courier", 22)

# Different sizes
font = pygame.font.SysFont("consolas", 26)        # Larger
small_font = pygame.font.SysFont("consolas", 14)  # Smaller

# Custom font file
font = pygame.font.Font("path/to/font.ttf", 22)
```

**Available System Fonts:**
```python
# List all available fonts
import pygame
pygame.init()
print(pygame.font.get_fonts())
```

### Visual Effects

#### Border Radius (rounded corners)

Food rendering:
```python
# Current (line 503)
pygame.draw.rect(screen, FOOD, food_rect, border_radius=8)

# Square food
pygame.draw.rect(screen, FOOD, food_rect, border_radius=0)

# More rounded
pygame.draw.rect(screen, FOOD, food_rect, border_radius=12)
```

Snake rendering:
```python
# Current (line 508)
pygame.draw.rect(screen, color, rect, border_radius=8)

# Adjust for different look
pygame.draw.rect(screen, color, rect, border_radius=4)  # Less rounded
```

#### Grid Visibility

To hide grid lines:
```python
def draw_grid(self):
    return  # Skip drawing grid
```

To make grid more prominent:
```python
GRID = (60, 60, 60)  # Lighter color
```

## Gameplay Configuration

### Initial Snake

Default starting position and length:
```python
def reset(self, mode="human"):
    cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2  # Center position
    self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]  # 3 segments
    self.direction = "RIGHT"
```

**To start with longer snake:**
```python
self.snake = [
    (cx, cy), (cx - 1, cy), (cx - 2, cy), 
    (cx - 3, cy), (cx - 4, cy)  # 5 segments
]
```

**To start in corner:**
```python
self.snake = [(2, 2), (1, 2), (0, 2)]
```

### Movement Rules

#### Allow 180° Turns

Current code prevents instant reversal:
```python
# Line 315
if self.next_direction != OPPOSITE[self.direction] or len(self.snake) == 1:
    self.direction = self.next_direction
```

To allow 180° turns (dangerous!):
```python
self.direction = self.next_direction  # Remove check
```

#### Wrap-Around Walls

Make walls wrap to opposite side:
```python
def in_bounds(self, pos):
    x, y = pos
    # Wrap around
    x = x % GRID_WIDTH
    y = y % GRID_HEIGHT
    return True  # Always in bounds
```

Then update collision detection:
```python
def step(self):
    # ... existing code ...
    head_x, head_y = self.snake[0]
    
    # Wrap coordinates
    new_head = (
        (head_x + dx) % GRID_WIDTH,
        (head_y + dy) % GRID_HEIGHT
    )
    
    # Remove wall collision check
    # if not self.in_bounds(new_head): ...
```

## Benchmark Configuration

### Number of Runs

```python
BENCHMARK_RUNS = 5  # Per algorithm
```

**Recommendations:**
- **Quick test**: 3 runs
- **Standard**: 5 runs (default)
- **Statistical**: 10+ runs
- **Research**: 20+ runs

### Maximum Steps

In `run_single_algorithm_game` method (line 346):
```python
def run_single_algorithm_game(self, mode, seed=None, max_steps=1500):
```

**To change:**
```python
max_steps = 1000   # Shorter games
max_steps = 2000   # Longer games
max_steps = 5000   # Extended games
```

**Effects:**
- Lower = faster benchmarks, potentially lower scores
- Higher = longer benchmarks, potentially higher scores
- Recommended: 1500-2000 for balanced results

### Algorithms to Benchmark

Modify `run_benchmark` method (line 372):
```python
def run_benchmark(self, runs_per_algorithm=BENCHMARK_RUNS):
    algorithms = ["bfs", "dfs", "greedy", "astar"]  # Current
    
    # To test only specific algorithms:
    algorithms = ["greedy", "astar"]  # Skip BFS and DFS
    
    # To add custom algorithm:
    algorithms = ["bfs", "dfs", "greedy", "astar", "custom"]
```

## AI Behavior Configuration

### Pathfinding Algorithm Selection

**Default Algorithm:**
```python
game = SnakeGame()
game.reset("astar")  # Start with A*
```

### Fallback Strategy

The fallback system can be tuned in `choose_fallback_move` (line 247):

**Current priority:**
1. Most open space
2. Closest to food

**To prioritize food distance:**
```python
score = (-food_dist, open_area)  # Negative food_dist for minimization
```

**To only consider space:**
```python
score = open_area  # Ignore food distance
```

**To add randomness:**
```python
import random
score = (open_area + random.randint(-5, 5), -food_dist)
```

### Heuristic Function

For Greedy and A*, modify `manhattan` method:

**Current (Manhattan distance):**
```python
def manhattan(self, a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

**Euclidean distance:**
```python
def euclidean(self, a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5
```

**Chebyshev distance:**
```python
def chebyshev(self, a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
```

**Weighted Manhattan:**
```python
def weighted_manhattan(self, a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return 1.5 * dx + dy  # Prefer horizontal movement
```

**Note:** Heuristic must be admissible for A* optimality.

## Keyboard Controls

### Adding New Controls

In `handle_key` method (line 420):

**Example: Add speed controls:**
```python
elif key == pygame.K_PLUS:
    global FPS
    FPS = min(FPS + 2, 60)
elif key == pygame.K_MINUS:
    FPS = max(FPS - 2, 1)
```

**Example: Add pause:**
```python
elif key == pygame.K_SPACE:
    self.paused = not self.paused
```

Then in `main()`:
```python
if not game.paused:
    game.step()
```

### Changing Control Scheme

**WASD instead of arrows:**
```python
if key == pygame.K_w:
    self.next_direction = "UP"
elif key == pygame.K_s:
    self.next_direction = "DOWN"
elif key == pygame.K_a:
    self.next_direction = "LEFT"
elif key == pygame.K_d:
    self.next_direction = "RIGHT"
```

## Performance Tuning

### Optimization for Large Grids

**Limit flood fill depth:**
```python
def flood_fill_space(self, start, blocked, max_depth=100):
    # ... existing code ...
    if count >= max_depth:
        return count
    # ... rest of code ...
```

**Cache pathfinding results:**
```python
def __init__(self):
    self.path_cache = {}
    # ... rest of init ...

def get_ai_move(self):
    cache_key = (tuple(self.snake), self.food)
    if cache_key in self.path_cache:
        return self.path_cache[cache_key]
    
    # ... compute move ...
    self.path_cache[cache_key] = move
    return move
```

### Disable Visualizations

For faster benchmarking without display:

**Skip rendering:**
```python
def run_single_algorithm_game(self, mode, seed=None, max_steps=1500, render=False):
    # ... existing code ...
    while not self.game_over and self.metrics.steps_survived < max_steps:
        self.step()
        if render:
            self.draw()
            clock.tick(FPS)
```

## Configuration Files

### Creating a Config File

Create `config.py`:
```python
# Display
CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 24
FPS = 12

# Colors
COLORS = {
    'bg': (18, 18, 18),
    'grid': (35, 35, 35),
    'snake_head': (80, 220, 120),
    'snake_body': (40, 170, 90),
    'food': (240, 80, 80),
}

# Gameplay
INITIAL_SNAKE_LENGTH = 3
ALLOW_REVERSE = False
WRAP_WALLS = False

# Benchmark
BENCHMARK_RUNS = 5
MAX_STEPS = 1500
```

Import in main file:
```python
import config

CELL_SIZE = config.CELL_SIZE
GRID_WIDTH = config.GRID_WIDTH
# ... etc
```

### JSON Configuration

Create `settings.json`:
```json
{
  "display": {
    "cell_size": 25,
    "grid_width": 24,
    "grid_height": 24,
    "fps": 12
  },
  "colors": {
    "background": [18, 18, 18],
    "snake_head": [80, 220, 120],
    "food": [240, 80, 80]
  },
  "benchmark": {
    "runs": 5,
    "max_steps": 1500
  }
}
```

Load in code:
```python
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

CELL_SIZE = settings['display']['cell_size']
FPS = settings['display']['fps']
```

## Command-Line Arguments

Add argument parsing:

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Snake AI')
    parser.add_argument('--mode', default='human', 
                       choices=['human', 'bfs', 'dfs', 'greedy', 'astar'])
    parser.add_argument('--fps', type=int, default=12)
    parser.add_argument('--grid-size', type=int, default=24)
    parser.add_argument('--benchmark', action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()
    
    global FPS, GRID_WIDTH, GRID_HEIGHT
    FPS = args.fps
    GRID_WIDTH = GRID_HEIGHT = args.grid_size
    
    game = SnakeGame()
    game.reset(args.mode)
    
    if args.benchmark:
        game.run_benchmark()
        return
    
    # ... rest of main loop ...
```

Run with:
```bash
python snake_ai_working_model.py --mode astar --fps 20
python snake_ai_working_model.py --benchmark --grid-size 32
```

## Example Configurations

### Speed Run Configuration

Fast games for quick testing:
```python
GRID_WIDTH = 16
GRID_HEIGHT = 16
FPS = 30
BENCHMARK_RUNS = 3
max_steps = 500
```

### Research Configuration

Thorough testing:
```python
GRID_WIDTH = 32
GRID_HEIGHT = 32
FPS = 12
BENCHMARK_RUNS = 20
max_steps = 3000
```

### Demo Configuration

Slow, easy to follow:
```python
GRID_WIDTH = 16
GRID_HEIGHT = 16
FPS = 6
# Larger cell size for visibility
CELL_SIZE = 40
```

### Challenge Configuration

Difficult gameplay:
```python
GRID_WIDTH = 32
GRID_HEIGHT = 32
FPS = 20
INITIAL_SNAKE_LENGTH = 10  # Start longer
```

## References

- [Getting Started](getting-started.md) - Installation and setup
- [Algorithm Guide](algorithms.md) - Understanding algorithms
- [API Reference](api-reference.md) - Code structure
- [Main README](../README.md) - Project overview
