# Benchmarking Guide

Comprehensive guide to running, interpreting, and analyzing benchmark results.

## Overview

The Snake AI project includes a sophisticated benchmarking system that allows you to:
- Compare algorithm performance objectively
- Collect statistical data across multiple runs
- Export results for further analysis
- Visualize performance differences in real-time

## Running Benchmarks

### Quick Start

1. Launch the game:
   ```bash
   python snake_ai_working_model.py
   ```

2. Press **B** to start benchmarking

3. Wait for all tests to complete (approximately 1-2 minutes)

4. View results by pressing **TAB**

### What Happens During Benchmarking

The benchmark process:
1. Tests each algorithm (BFS, DFS, Greedy, A*) sequentially
2. Runs each algorithm 5 times (configurable)
3. Uses consistent random seeds for fair comparison
4. Limits each game to 1500 steps maximum
5. Collects detailed performance metrics
6. Calculates summary statistics
7. Exports all data to CSV file
8. Displays results overlay

### Benchmark Configuration

Modify these constants in `snake_ai_working_model.py`:

```python
BENCHMARK_RUNS = 5      # Number of runs per algorithm
max_steps = 1500        # Maximum steps per game (in run_single_algorithm_game)
```

**Recommendations:**
- **Quick testing**: `BENCHMARK_RUNS = 3`, `max_steps = 1000`
- **Standard**: `BENCHMARK_RUNS = 5`, `max_steps = 1500`
- **Thorough**: `BENCHMARK_RUNS = 10`, `max_steps = 2000`

## Understanding Metrics

### Per-Run Metrics

Each benchmark run records:

| Metric | Description | Good Value | Units |
|--------|-------------|------------|-------|
| **Score** | Food items collected | Higher is better | count |
| **Steps Survived** | Total moves made | Higher is better (up to max) | count |
| **Foods Collected** | Same as score | Higher is better | count |
| **Avg Nodes Expanded** | Mean nodes explored per decision | Lower is more efficient | count |
| **Avg Decision Time** | Mean computation time per decision | Lower is faster | milliseconds |
| **Max Snake Length** | Longest snake achieved | Higher is better | count |

### Summary Statistics

For each algorithm, the benchmark calculates:

| Statistic | Description | Formula |
|-----------|-------------|---------|
| **Avg Score** | Mean across all runs | `sum(scores) / num_runs` |
| **Avg Steps** | Mean survival steps | `sum(steps) / num_runs` |
| **Avg Foods** | Mean food collected | `sum(foods) / num_runs` |
| **Avg Nodes** | Mean nodes expanded | `sum(nodes) / num_runs` |
| **Avg ms** | Mean decision time | `sum(times) / num_runs` |
| **Best Score** | Highest score in any run | `max(scores)` |
| **Best Steps** | Longest survival | `max(steps)` |

## Interpreting Results

### Example Benchmark Results

From actual benchmark data:

```
Algo    Avg Score   Avg Steps   Avg Foods   Avg Nodes   Avg ms    Best Score
BFS     75.4        1357.4      75.4        58.6        0.13      84
DFS     0.4         1500.0      0.4         289.4       0.29      1
Greedy  79.0        1462.2      79.0        59.4        0.03      83
A*      81.0        1500.0      81.0        85.0        0.06      84
```

### Analysis

#### Performance Rankings

**By Score (Quality):**
1. **A*** - 81.0 (best)
2. Greedy - 79.0
3. BFS - 75.4
4. DFS - 0.4 (very poor)

**By Speed (Efficiency):**
1. **Greedy** - 0.03ms (fastest)
2. A* - 0.06ms
3. BFS - 0.13ms
4. DFS - 0.29ms (slowest)

**By Node Efficiency:**
1. **BFS** - 58.6 nodes (most efficient search)
2. Greedy - 59.4 nodes
3. A* - 85.0 nodes
4. DFS - 289.4 nodes (very inefficient)

#### Key Insights

**A* (Recommended Overall):**
- ✓ Highest average score
- ✓ Consistent high performance
- ✓ Optimal pathfinding
- ✓ Good balance of speed and quality
- Ideal for production use

**Greedy (Speed Priority):**
- ✓ Fastest decision-making
- ✓ Nearly as good as A* in practice
- ✓ Excellent for real-time requirements
- ✗ Slightly lower scores than A*
- Good when speed matters most

**BFS (Educational):**
- ✓ Guaranteed shortest paths
- ✓ Predictable behavior
- ✗ Slower than A* and Greedy
- ✗ Lower scores than optimal algorithms
- Good for learning/demonstration

**DFS (Avoid):**
- ✗ Extremely poor performance
- ✗ Rarely collects food
- ✗ Slowest decision-making
- ✗ Not suitable for Snake game
- Only useful for algorithm comparison

### What Makes a Good Run?

**Excellent Run:**
- Score: 80+
- Steps: Reaches 1500 (max)
- Avg nodes: < 100
- Avg time: < 0.1ms
- No premature game-overs

**Good Run:**
- Score: 60-79
- Steps: 1000-1499
- Avg nodes: < 200
- Avg time: < 0.2ms

**Poor Run:**
- Score: < 20
- Steps: < 500
- Avg nodes: > 300
- Frequent self-collisions

### Variance Analysis

**Low Variance (Consistent):**
- A* and BFS typically show consistent scores
- Indicates reliable algorithm behavior
- Preferred for production

**High Variance (Unpredictable):**
- DFS shows high variance
- Greedy can vary based on food placement
- Less desirable for critical applications

## CSV Export Format

### File Location

Results are saved to: `snake_ai_benchmark_results.csv`

### CSV Structure

```csv
algorithm,run_number,score,steps_survived,foods_collected,avg_nodes_expanded,avg_decision_ms,max_snake_length
bfs,1,80,1500,80,37.0,0.143,83
bfs,2,62,1081,62,1.0,0.144,65
...
```

### Columns Explained

- **algorithm**: Name of search algorithm (bfs, dfs, greedy, astar)
- **run_number**: Sequential run identifier (1-N)
- **score**: Final score (food items collected)
- **steps_survived**: Total steps before game over or max limit
- **foods_collected**: Same as score
- **avg_nodes_expanded**: Mean nodes expanded per pathfinding decision
- **avg_decision_ms**: Mean computation time per decision (milliseconds)
- **max_snake_length**: Longest snake length achieved (starts at 3)

## Advanced Analysis

### Importing CSV for Analysis

#### Python with Pandas

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('snake_ai_benchmark_results.csv')

# Group by algorithm
summary = df.groupby('algorithm').agg({
    'score': ['mean', 'std', 'min', 'max'],
    'avg_decision_ms': ['mean', 'std'],
    'steps_survived': ['mean']
}).round(2)

print(summary)

# Plot scores
df.boxplot(column='score', by='algorithm', figsize=(10, 6))
plt.title('Score Distribution by Algorithm')
plt.ylabel('Score')
plt.show()
```

#### Python with Statistics Module

```python
import csv
import statistics

# Load data
results = {'bfs': [], 'dfs': [], 'greedy': [], 'astar': []}

with open('snake_ai_benchmark_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        algo = row['algorithm']
        score = int(row['score'])
        results[algo].append(score)

# Calculate statistics
for algo, scores in results.items():
    print(f"{algo.upper()}:")
    print(f"  Mean: {statistics.mean(scores):.2f}")
    print(f"  Median: {statistics.median(scores):.2f}")
    print(f"  Std Dev: {statistics.stdev(scores):.2f}")
    print(f"  Range: {min(scores)} - {max(scores)}")
```

#### Excel / Google Sheets

1. Open CSV in Excel/Sheets
2. Create pivot table:
   - Rows: algorithm
   - Values: AVERAGE(score), AVERAGE(avg_decision_ms), MAX(score)
3. Create charts:
   - Bar chart comparing average scores
   - Line chart showing score over runs
   - Scatter plot: decision time vs score

### Statistical Tests

#### Comparing Algorithm Performance

```python
from scipy import stats

# Load scores for two algorithms
bfs_scores = [80, 62, 84, 70, 81]
astar_scores = [76, 83, 84, 81, 81]

# T-test
t_stat, p_value = stats.ttest_ind(bfs_scores, astar_scores)
print(f"T-statistic: {t_stat:.3f}")
print(f"P-value: {p_value:.3f}")

if p_value < 0.05:
    print("Significantly different")
else:
    print("No significant difference")
```

#### Correlation Analysis

```python
import pandas as pd

df = pd.read_csv('snake_ai_benchmark_results.csv')

# Correlation between nodes expanded and decision time
corr = df['avg_nodes_expanded'].corr(df['avg_decision_ms'])
print(f"Correlation: {corr:.3f}")

# Correlation between steps survived and score
corr2 = df['steps_survived'].corr(df['score'])
print(f"Survival-Score Correlation: {corr2:.3f}")
```

## Custom Benchmarks

### Testing Specific Scenarios

#### Different Grid Sizes

Modify constants and run benchmark:

```python
# In snake_ai_working_model.py
GRID_WIDTH = 16   # Smaller grid
GRID_HEIGHT = 16

# Run benchmarks to see how algorithms perform on smaller grids
```

#### Different Time Limits

```python
# Shorter games
game.run_single_algorithm_game("astar", max_steps=500)

# Longer games
game.run_single_algorithm_game("astar", max_steps=3000)
```

#### Fixed Seeds for Reproducibility

```python
game = SnakeGame()
results = []

for seed in range(10):
    result = game.run_single_algorithm_game("astar", seed=seed)
    results.append(result)
    print(f"Seed {seed}: Score = {result.score}")
```

### Creating Custom Metrics

```python
class ExtendedMetrics(Metrics):
    total_backtrack_moves: int = 0
    food_distance_sum: int = 0
    close_calls: int = 0  # Times snake almost hit itself

# Use in game
game.metrics = ExtendedMetrics(algorithm="astar")
```

## Benchmark Best Practices

### Do's

✓ **Run multiple iterations** - At least 5 runs per algorithm for statistical validity

✓ **Use consistent seeds** - For fair comparison across algorithms

✓ **Set reasonable limits** - 1500 steps is usually sufficient

✓ **Export data** - Always save CSV for later analysis

✓ **Consider variance** - Look at consistency, not just averages

✓ **Test different scenarios** - Grid sizes, speeds, etc.

### Don'ts

✗ **Don't compare single runs** - Statistical outliers are common

✗ **Don't ignore outliers completely** - They reveal edge cases

✗ **Don't optimize for benchmarks only** - Real-world use matters

✗ **Don't assume fastest = best** - Quality matters too

✗ **Don't forget to document** - Record test conditions and parameters

## Troubleshooting

### Benchmark Takes Too Long

**Problem**: Benchmarking takes several minutes

**Solutions:**
1. Reduce `BENCHMARK_RUNS` to 3
2. Lower `max_steps` to 1000
3. Increase `FPS` during benchmarks (though this shouldn't affect results)

### Inconsistent Results

**Problem**: Results vary significantly between benchmark runs

**Causes:**
- Using different random seeds
- System performance variations
- Not enough runs for statistical validity

**Solutions:**
1. Increase `BENCHMARK_RUNS` to 10+
2. Use fixed seeds
3. Close other applications
4. Run benchmarks multiple times and average

### DFS Shows Score of 0

**Problem**: DFS consistently scores 0

**Explanation**: This is expected! DFS performs poorly in the Snake game because:
- It takes unnecessarily long paths
- Traps itself frequently
- Rarely reaches food before self-collision

### CSV File Not Found

**Problem**: `snake_ai_benchmark_results.csv` doesn't exist

**Solutions:**
1. Check current directory
2. Ensure benchmark completed successfully
3. Check file permissions
4. Run benchmark again with `B` key

## Visualization Tips

### In-Game Overlay

The benchmark overlay shows:
- Summary statistics table
- Algorithm names and key metrics
- File save confirmation

Press **TAB** to toggle visibility.

### External Visualization

#### Using Python (Matplotlib)

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('snake_ai_benchmark_results.csv')

# Score comparison
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Box plot of scores
df.boxplot(column='score', by='algorithm', ax=axes[0, 0])
axes[0, 0].set_title('Score Distribution')

# 2. Decision time comparison
df.groupby('algorithm')['avg_decision_ms'].mean().plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('Average Decision Time')

# 3. Nodes expanded
df.groupby('algorithm')['avg_nodes_expanded'].mean().plot(kind='bar', ax=axes[1, 0])
axes[1, 0].set_title('Average Nodes Expanded')

# 4. Steps survived
df.groupby('algorithm')['steps_survived'].mean().plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('Average Steps Survived')

plt.tight_layout()
plt.savefig('benchmark_analysis.png')
plt.show()
```

## Performance Optimization Research

Use benchmarks to investigate:

### Heuristic Effectiveness

Test different heuristics for A* and Greedy:
- Manhattan distance (current)
- Euclidean distance
- Diagonal distance
- Custom weighted heuristics

### Grid Size Impact

How do algorithms scale?
- Small grids (12x12)
- Medium grids (24x24) - current
- Large grids (48x48)

### Speed vs Quality Tradeoff

Measure correlation between:
- Decision time and score
- Nodes expanded and optimality
- Path length and safety

## References

- [Algorithm Guide](algorithms.md) - Understanding algorithm behavior
- [API Reference](api-reference.md) - Implementing custom benchmarks
- [Configuration](configuration.md) - Adjusting benchmark parameters
- [Main README](../README.md) - Project overview
