# Contributing to Snake AI

Thank you for your interest in contributing to the Snake AI project! This guide will help you get started.

## Ways to Contribute

There are many ways to contribute to this project:

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have an idea for improvement?
- **Improve documentation** - Help others understand the project
- **Write code** - Implement new features or fix bugs
- **Optimize algorithms** - Improve performance
- **Add algorithms** - Implement new search strategies
- **Create tutorials** - Help others learn

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/snake-ai.git
cd snake-ai
```

### 2. Set Up Development Environment

```bash
# Install dependencies
pip install pygame

# Optional: Install development tools
pip install pylint black pytest
```

### 3. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

## Code Style Guidelines

### Python Style

Follow PEP 8 guidelines:

**Good:**
```python
def calculate_distance(point_a, point_b):
    """Calculate Manhattan distance between two points."""
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])
```

**Bad:**
```python
def calc_dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
```

### Naming Conventions

- **Functions/Methods**: `snake_case`
  - `get_ai_move()`, `spawn_food()`, `calculate_distance()`

- **Classes**: `PascalCase`
  - `SnakeGame`, `BenchmarkResult`, `Metrics`

- **Constants**: `UPPER_CASE`
  - `GRID_WIDTH`, `FPS`, `CELL_SIZE`

- **Variables**: `snake_case`
  - `current_position`, `path_length`, `game_over`

### Docstrings

Use docstrings for all public functions and classes:

```python
def bfs(self, start, goal, blocked):
    """
    Breadth-First Search pathfinding algorithm.
    
    Args:
        start (tuple): Starting (x, y) position
        goal (tuple): Target (x, y) position
        blocked (set): Set of blocked positions
    
    Returns:
        tuple: (path_list, nodes_expanded_count)
            - path_list: List of positions from start to goal
            - nodes_expanded_count: Number of nodes explored
    
    Example:
        >>> path, nodes = game.bfs((0,0), (5,5), set())
        >>> print(len(path))
        11
    """
    # Implementation
```

### Comments

Write clear, helpful comments:

**Good:**
```python
# Calculate available space to avoid trapping the snake
open_area = self.flood_fill_space(next_pos, blocked)
```

**Bad:**
```python
# Calculate space
open_area = self.flood_fill_space(next_pos, blocked)
```

### Code Formatting

Use Black formatter (or similar):

```bash
# Format all Python files
black snake_ai_working_model.py

# Check without modifying
black --check snake_ai_working_model.py
```

## Adding New Features

### Adding a New Algorithm

1. **Implement the algorithm method:**

```python
def dijkstra(self, start, goal, blocked):
    """
    Dijkstra's pathfinding algorithm.
    
    Args:
        start: Starting position
        goal: Target position
        blocked: Set of blocked positions
    
    Returns:
        tuple: (path, nodes_expanded)
    """
    import heapq
    
    open_heap = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}
    expanded = 0
    
    while open_heap:
        current_cost, current = heapq.heappop(open_heap)
        expanded += 1
        
        if current == goal:
            return self.reconstruct_path(came_from, start, goal), expanded
        
        for next_pos in self.safe_neighbors(current, blocked):
            new_cost = cost_so_far[current] + 1
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                came_from[next_pos] = current
                heapq.heappush(open_heap, (new_cost, next_pos))
    
    return [], expanded
```

2. **Add to AI move selection:**

```python
def get_ai_move(self):
    # ... existing code ...
    
    if algo == "bfs":
        path, expanded = self.bfs(head, self.food, blocked)
    elif algo == "dijkstra":  # Add new algorithm
        path, expanded = self.dijkstra(head, self.food, blocked)
    # ... rest of code ...
```

3. **Add keyboard control:**

```python
def handle_key(self, key):
    # ... existing code ...
    elif key == pygame.K_5:  # Add new key
        self.reset("dijkstra")
```

4. **Update benchmark:**

```python
def run_benchmark(self, runs_per_algorithm=BENCHMARK_RUNS):
    algorithms = ["bfs", "dfs", "greedy", "astar", "dijkstra"]  # Add to list
    # ... rest of code ...
```

5. **Update documentation:**
   - Add to README.md
   - Add to docs/algorithms.md
   - Update control reference

### Adding Metrics

1. **Extend Metrics dataclass:**

```python
@dataclass
class Metrics:
    # ... existing fields ...
    turns_made: int = 0
    average_path_efficiency: float = 0.0
```

2. **Update metric tracking:**

```python
def step(self):
    # ... existing code ...
    
    # Track turns
    if self.direction != old_direction:
        self.metrics.turns_made += 1
```

3. **Display in UI:**

```python
def draw(self):
    # ... existing code ...
    
    line_extra = f"Turns: {self.metrics.turns_made}"
    screen.blit(small_font.render(line_extra, True, SUBTEXT), (12, GRID_HEIGHT * CELL_SIZE + 80))
```

### Adding Visualization Features

Example: Highlight dangerous cells

```python
def draw_danger_zones(self):
    """Highlight cells adjacent to snake body."""
    if self.mode == "human":
        return
    
    danger_cells = set()
    for segment in self.snake[1:]:  # Skip head
        for neighbor in self.neighbors(segment):
            if neighbor not in self.snake:
                danger_cells.add(neighbor)
    
    for cell in danger_cells:
        rx = cell[0] * CELL_SIZE + 8
        ry = cell[1] * CELL_SIZE + 8
        pygame.draw.rect(screen, DANGER, (rx, ry, CELL_SIZE - 16, CELL_SIZE - 16), 
                        border_radius=4)

# Call in draw()
def draw(self):
    # ... after draw_grid() ...
    self.draw_danger_zones()
    # ... rest of drawing ...
```

## Testing

### Manual Testing

Before submitting:

1. **Test all modes:**
   - Human mode works
   - Each AI algorithm runs without errors
   - Mode switching works correctly

2. **Test controls:**
   - All keyboard shortcuts work
   - Game responds appropriately

3. **Test benchmarks:**
   - Benchmark completes successfully
   - CSV exports correctly
   - Results overlay displays properly

4. **Test edge cases:**
   - Snake hitting walls
   - Snake hitting itself
   - No available moves
   - Food spawning near snake

### Automated Testing

Create `test_snake_ai.py`:

```python
import unittest
from snake_ai_working_model import SnakeGame

class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame()
    
    def test_initial_state(self):
        """Test game initializes correctly."""
        self.assertEqual(len(self.game.snake), 3)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.mode, "human")
    
    def test_in_bounds(self):
        """Test boundary checking."""
        self.assertTrue(self.game.in_bounds((0, 0)))
        self.assertTrue(self.game.in_bounds((23, 23)))
        self.assertFalse(self.game.in_bounds((-1, 0)))
        self.assertFalse(self.game.in_bounds((24, 0)))
    
    def test_manhattan_distance(self):
        """Test distance calculation."""
        self.assertEqual(self.game.manhattan((0, 0), (3, 4)), 7)
        self.assertEqual(self.game.manhattan((5, 5), (5, 5)), 0)
    
    def test_bfs_finds_path(self):
        """Test BFS pathfinding."""
        path, nodes = self.game.bfs((0, 0), (5, 5), set())
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (5, 5))
    
    def test_algorithm_switching(self):
        """Test mode switching."""
        self.game.reset("astar")
        self.assertEqual(self.game.mode, "astar")
        self.assertEqual(self.game.metrics.algorithm, "astar")

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest test_snake_ai.py
# or
python test_snake_ai.py
```

## Submitting Changes

### 1. Commit Your Changes

Follow commit message conventions:

**Format:**
```
<type>: <short description>

<optional detailed description>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `perf`: Performance improvements

**Examples:**

```bash
# Good commit messages
git commit -m "feat: add Dijkstra's algorithm implementation"
git commit -m "fix: prevent snake from reversing direction"
git commit -m "docs: update algorithm comparison table"
git commit -m "perf: cache pathfinding results for faster decisions"

# Bad commit messages
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "asdf"
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test these changes?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Benchmarks run successfully
```

### 4. Address Review Comments

- Respond to feedback promptly
- Make requested changes
- Push updates to the same branch
- Request re-review when ready

## Bug Reports

### How to Report a Bug

Create an issue with:

**Title:** Clear, concise description

**Description:**
```markdown
## Expected Behavior
What should happen?

## Actual Behavior
What actually happens?

## Steps to Reproduce
1. Run the game
2. Press key X
3. Observe error Y

## Environment
- OS: Windows 10 / macOS 12 / Ubuntu 20.04
- Python version: 3.9.5
- Pygame version: 2.5.0

## Additional Context
Screenshots, error messages, etc.
```

### Common Issues

**Issue**: Game crashes on startup
**Check**: Pygame installed? Python version 3.7+?

**Issue**: Benchmark produces errors
**Check**: Sufficient disk space for CSV? File permissions?

**Issue**: AI behaves unexpectedly
**Check**: Algorithm implementation correct? Fallback system triggered?

## Feature Requests

When suggesting features:

1. **Explain the use case** - Why is this useful?
2. **Describe the feature** - What should it do?
3. **Consider alternatives** - Other ways to achieve the goal?
4. **Impact assessment** - Breaking changes? Performance impact?

**Example:**
```markdown
## Feature: Hamiltonian Cycle Algorithm

### Use Case
Hamiltonian cycles can guarantee the snake never loses by following 
a predetermined path that covers all cells.

### Description
Implement Hamilton cycle pathfinding as an alternative strategy that 
prioritizes safety over efficiency.

### API
- Add `hamiltonian()` method to SnakeGame
- Add keyboard shortcut (K_6)
- Include in benchmarks

### Performance Considerations
- Initial cycle calculation may be slow on large grids
- Gameplay will be slower but extremely safe
- Should include toggle for "shortcut mode"
```

## Code Review Checklist

When reviewing code (or preparing for review):

**Functionality:**
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] No obvious bugs
- [ ] Algorithm correctness verified

**Code Quality:**
- [ ] Follows project style
- [ ] Well-documented
- [ ] No code duplication
- [ ] Efficient implementation
- [ ] Readable and maintainable

**Testing:**
- [ ] Tested manually
- [ ] Tests added (if applicable)
- [ ] Benchmarks still work
- [ ] No regressions

**Documentation:**
- [ ] README updated
- [ ] API docs updated
- [ ] Comments clear
- [ ] Examples provided

## Development Tools

### Recommended Tools

**Linting:**
```bash
pip install pylint
pylint snake_ai_working_model.py
```

**Formatting:**
```bash
pip install black
black snake_ai_working_model.py
```

**Type Checking:**
```bash
pip install mypy
mypy snake_ai_working_model.py
```

**Testing:**
```bash
pip install pytest
pytest test_snake_ai.py
```

### Git Hooks

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Format code before commit
black snake_ai_working_model.py

# Run tests
python -m pytest test_snake_ai.py

if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Project Structure

```
snake-ai/
├── snake_ai_working_model.py      # Main implementation
├── snake_ai_benchmark_results.csv # Generated results
├── test_snake_ai.py               # Tests (if created)
├── config.py                      # Config (if created)
├── README.md                      # Main documentation
├── .gitignore                     # Git ignore rules
└── docs/                          # Documentation
    ├── index.md                   # Docs home
    ├── getting-started.md         # Setup guide
    ├── algorithms.md              # Algorithm details
    ├── api-reference.md           # Code documentation
    ├── benchmarking.md            # Benchmark guide
    ├── configuration.md           # Config options
    └── contributing.md            # This file
```

## Community Guidelines

- **Be respectful** - Treat everyone with respect
- **Be constructive** - Provide helpful feedback
- **Be patient** - Contributors have varying experience levels
- **Be collaborative** - Work together toward common goals

## Questions?

If you have questions:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with the "question" label
4. Provide context and what you've tried

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor list

Thank you for contributing to Snake AI!

## References

- [Main README](../README.md) - Project overview
- [API Reference](api-reference.md) - Code documentation
- [Algorithm Guide](algorithms.md) - Algorithm details
