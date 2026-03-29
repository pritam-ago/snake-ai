# Algorithm Guide

This document provides detailed explanations of each search algorithm implemented in the Snake AI project.

## Overview

All algorithms solve the same problem: finding a path from the snake's head to the food while avoiding the snake's body. However, they differ in their approach, guarantees, and performance characteristics.

## Algorithm Comparison Table

| Algorithm | Complete? | Optimal? | Time Complexity | Space Complexity | Best For |
|-----------|-----------|----------|-----------------|------------------|----------|
| BFS | Yes | Yes | O(b^d) | O(b^d) | Shortest path guarantee |
| DFS | Yes* | No | O(b^m) | O(bm) | Memory-constrained scenarios |
| Greedy | No | No | O(b^d) | O(b^d) | Fast decisions |
| A* | Yes | Yes | O(b^d) | O(b^d) | Optimal + efficient |

*DFS is complete in finite spaces with cycle detection

Where:
- `b` = branching factor (max 4 in this grid)
- `d` = depth of solution
- `m` = maximum depth of search tree

## Breadth-First Search (BFS)

### How It Works

BFS explores the grid level by level, like ripples spreading in water:

1. Start at the snake's head
2. Explore all neighbors at distance 1
3. Then explore all neighbors at distance 2
4. Continue until food is found

### Implementation Details

```python
def bfs(self, start, goal, blocked):
    q = deque([start])           # Queue for frontier
    came_from = {}               # Track path
    visited = {start}            # Avoid revisiting
    expanded = 0
    
    while q:
        current = q.popleft()    # FIFO: First in, first out
        expanded += 1
        
        if current == goal:
            return self.reconstruct_path(came_from, start, goal), expanded
            
        for nxt in self.safe_neighbors(current, blocked):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                q.append(nxt)
    
    return [], expanded
```

### Characteristics

**Strengths:**
- ✓ Guarantees shortest path
- ✓ Complete (always finds solution if one exists)
- ✓ Predictable behavior

**Weaknesses:**
- ✗ Can be slower than A* or Greedy
- ✗ Explores many unnecessary nodes
- ✗ High memory usage for large grids

**Typical Performance:**
- Average Score: ~75
- Average Decision Time: ~0.13 ms
- Nodes Expanded: Varies (1-176 per decision)

### When to Use

Use BFS when:
- You need the shortest path guarantee
- The grid is small to medium sized
- Memory is not a major constraint

## Depth-First Search (DFS)

### How It Works

DFS explores as far as possible along each branch before backtracking:

1. Start at the snake's head
2. Pick a neighbor and go as deep as possible
3. When stuck, backtrack and try another branch
4. Continue until food is found

### Implementation Details

```python
def dfs(self, start, goal, blocked):
    stack = [start]              # Stack for frontier
    came_from = {}
    visited = {start}
    expanded = 0
    
    while stack:
        current = stack.pop()    # LIFO: Last in, first out
        expanded += 1
        
        if current == goal:
            return self.reconstruct_path(came_from, start, goal), expanded
            
        for nxt in reversed(self.safe_neighbors(current, blocked)):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                stack.append(nxt)
    
    return [], expanded
```

### Characteristics

**Strengths:**
- ✓ Low memory usage (only stores current path)
- ✓ Simple to implement
- ✓ Can find solutions quickly if lucky

**Weaknesses:**
- ✗ **Does not find shortest path**
- ✗ Can get stuck in long winding paths
- ✗ Very poor performance in Snake game
- ✗ Unpredictable behavior

**Typical Performance:**
- Average Score: ~0.4 (very poor!)
- Average Decision Time: ~0.29 ms
- Nodes Expanded: 200-400 per decision

### Why DFS Performs Poorly

In the Snake game, DFS tends to:
1. Take unnecessarily long paths to the food
2. Trap itself by following winding routes
3. Create dangerous situations with its body
4. Rarely achieve high scores

### When to Use

DFS is **not recommended** for Snake AI, but might be useful for:
- Maze generation
- Topological sorting
- Cycle detection
- Situations where any solution is acceptable (not optimal)

## Greedy Best-First Search

### How It Works

Greedy search uses a heuristic (estimated distance to goal) to guide its search:

1. Start at the snake's head
2. Always explore the neighbor closest to the food first
3. Use Manhattan distance as the heuristic
4. Continue until food is found

### Implementation Details

```python
def greedy(self, start, goal, blocked):
    heap = []
    heapq.heappush(heap, (self.manhattan(start, goal), start))
    came_from = {}
    visited = {start}
    expanded = 0
    
    while heap:
        _, current = heapq.heappop(heap)    # Pop lowest h(n)
        expanded += 1
        
        if current == goal:
            return self.reconstruct_path(came_from, start, goal), expanded
            
        for nxt in self.safe_neighbors(current, blocked):
            if nxt not in visited:
                visited.add(nxt)
                came_from[nxt] = current
                h = self.manhattan(nxt, goal)    # Heuristic only
                heapq.heappush(heap, (h, nxt))
    
    return [], expanded
```

### Heuristic Function

Manhattan distance (L1 distance):
```python
def manhattan(self, a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

This is admissible (never overestimates) in a grid with 4-directional movement.

### Characteristics

**Strengths:**
- ✓ **Fastest decision-making** (~0.03 ms)
- ✓ Very good performance in practice
- ✓ Intuitive behavior (moves toward food)
- ✓ Expands fewer nodes than BFS

**Weaknesses:**
- ✗ Not guaranteed to find shortest path
- ✗ Can get trapped in local optima
- ✗ Not complete in all scenarios

**Typical Performance:**
- Average Score: ~79
- Average Decision Time: ~0.03 ms (fastest!)
- Nodes Expanded: Usually very few (1-253)

### When to Use

Use Greedy when:
- Speed is critical
- Near-optimal solutions are acceptable
- The heuristic is reliable
- Real-time performance matters

## A* Search

### How It Works

A* combines BFS's optimality with Greedy's efficiency:

1. Evaluate nodes using `f(n) = g(n) + h(n)`
   - `g(n)` = actual cost from start to n
   - `h(n)` = estimated cost from n to goal
2. Always expand the node with lowest `f(n)`
3. Guaranteed to find optimal path if `h(n)` is admissible

### Implementation Details

```python
def astar(self, start, goal, blocked):
    open_heap = []
    heapq.heappush(open_heap, (0, start))
    came_from = {}
    g_score = {start: 0}
    expanded = 0
    
    while open_heap:
        _, current = heapq.heappop(open_heap)
        expanded += 1
        
        if current == goal:
            return self.reconstruct_path(came_from, start, goal), expanded
            
        for nxt in self.safe_neighbors(current, blocked):
            tentative_g = g_score[current] + 1
            
            if tentative_g < g_score.get(nxt, float("inf")):
                came_from[nxt] = current
                g_score[nxt] = tentative_g
                f_score = tentative_g + self.manhattan(nxt, goal)
                heapq.heappush(open_heap, (f_score, nxt))
    
    return [], expanded
```

### Cost Function Breakdown

- **g(n)**: Steps taken from start to current node
  - Always accurate (based on actual path)
  
- **h(n)**: Manhattan distance to goal
  - Admissible (never overestimates)
  - Consistent (satisfies triangle inequality)

- **f(n) = g(n) + h(n)**: Total estimated cost
  - Balances exploration and exploitation
  - Guides search efficiently toward goal

### Characteristics

**Strengths:**
- ✓ **Optimal** (finds shortest path)
- ✓ **Complete** (always finds solution if exists)
- ✓ More efficient than BFS
- ✓ Best overall performance in benchmarks
- ✓ Predictable and reliable

**Weaknesses:**
- ✗ Slower than Greedy (~0.06 ms vs 0.03 ms)
- ✗ More complex to implement
- ✗ Requires admissible heuristic

**Typical Performance:**
- Average Score: ~81 (highest!)
- Average Decision Time: ~0.06 ms
- Nodes Expanded: Moderate (6-208)

### When to Use

Use A* when:
- You need optimal solutions
- Computational resources are sufficient
- A good heuristic is available
- **This is the recommended default for Snake AI**

## Fallback Safety System

All algorithms use a fallback system when no direct path exists:

### How It Works

```python
def choose_fallback_move(self):
    head = self.snake[0]
    candidates = []
    
    # For each possible direction
    for name, (dx, dy) in DIRECTIONS.items():
        # Skip if it's opposite to current direction
        # Skip if out of bounds or hits body
        
        # Calculate open space using flood fill
        open_area = self.flood_fill_space(nxt, future_blocked)
        food_dist = self.manhattan(nxt, self.food)
        
        # Prioritize: more space > closer to food
        score = (open_area, -food_dist)
        candidates.append((score, name))
    
    # Choose move with most open space
    candidates.sort(reverse=True)
    return candidates[0][1] if candidates else None
```

### Why This Matters

Without fallback, the snake would:
- Hit walls when no path exists
- Trap itself in corners
- Die prematurely

With fallback, the snake:
- Avoids immediate death
- Seeks open space
- Waits for better opportunities
- Achieves much higher scores

## Visualization

When watching algorithms in action, observe:

1. **Path Highlighting** (blue cells)
   - Shows planned route to food
   - BFS: Shortest path, many nodes explored
   - DFS: Winding paths, unpredictable
   - Greedy: Direct path, few nodes
   - A*: Optimal path, efficient exploration

2. **Node Expansion Count**
   - How many cells were examined
   - Lower = more efficient
   - Higher = more thorough

3. **Decision Time**
   - Milliseconds to compute path
   - Critical for real-time performance
   - Greedy fastest, DFS slowest

## Algorithm Selection Guide

Choose your algorithm based on priorities:

| Priority | Recommended Algorithm |
|----------|----------------------|
| Optimal path | A* or BFS |
| Fastest decisions | Greedy |
| Best score | A* |
| Educational demo | Compare all |
| Production game | A* |
| Memory constrained | DFS (though not recommended) |

## Advanced Topics

### Heuristic Design

A good heuristic should be:
- **Admissible**: Never overestimate cost
- **Consistent**: h(n) ≤ cost(n,n') + h(n')
- **Informative**: Close to actual cost

Manhattan distance is ideal for grid-based movement.

### Dynamic Environment Challenges

Snake game is unique because:
1. **Moving obstacles**: Snake body changes position
2. **Growing obstacles**: Snake gets longer
3. **Changing goals**: New food spawns after eating
4. **Self-created problems**: Snake can trap itself

These factors make even optimal algorithms struggle without fallback strategies.

## References

- [Main README](../README.md) - Project overview
- [Benchmarking Guide](benchmarking.md) - Performance comparison
- [API Reference](api-reference.md) - Implementation details
