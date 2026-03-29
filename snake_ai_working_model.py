import pygame
import random
import sys
import time
from collections import deque
from dataclasses import dataclass
import heapq

# ============================================================
# Snake AI Working Model
# Modes: human, bfs, dfs, greedy, astar
# Run:
#   pip install pygame
#   python snake_ai_working_model.py
# Controls:
#   H = Human mode
#   1 = BFS
#   2 = DFS
#   3 = Greedy Best-First Search
#   4 = A* Search
#   R = Restart
#   ESC = Quit
# ============================================================

CELL_SIZE = 25
GRID_WIDTH = 24
GRID_HEIGHT = 24
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + 90
FPS = 12

BG = (18, 18, 18)
GRID = (35, 35, 35)
SNAKE_HEAD = (80, 220, 120)
SNAKE_BODY = (40, 170, 90)
FOOD = (240, 80, 80)
TEXT = (240, 240, 240)
SUBTEXT = (180, 180, 180)
PANEL = (28, 28, 28)
PATH_COLOR = (80, 130, 255)
DANGER = (255, 170, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI - Search Algorithms")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)
small_font = pygame.font.SysFont("consolas", 16)

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


@dataclass
class Metrics:
    algorithm: str = "human"
    nodes_expanded: int = 0
    last_path_length: int = 0
    foods_collected: int = 0
    score: int = 0
    steps_survived: int = 0
    computation_ms: float = 0.0


class SnakeGame:
    def __init__(self):
        self.reset("human")

    def reset(self, mode="human"):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.food = self.spawn_food()
        self.game_over = False
        self.mode = mode
        self.metrics = Metrics(algorithm=mode)
        self.cached_path = []
        self.last_reason = ""

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                return pos

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def is_occupied(self, pos, snake_body=None):
        body = snake_body if snake_body is not None else self.snake
        return pos in body

    def neighbors(self, pos):
        x, y = pos
        cands = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ]
        return [p for p in cands if self.in_bounds(p)]

    def safe_neighbors(self, pos, blocked):
        return [n for n in self.neighbors(pos) if n not in blocked]

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, start, goal):
        if goal not in came_from and goal != start:
            return []
        cur = goal
        path = [cur]
        while cur != start:
            cur = came_from[cur]
            path.append(cur)
        path.reverse()
        return path

    def bfs(self, start, goal, blocked):
        q = deque([start])
        came_from = {}
        visited = {start}
        expanded = 0

        while q:
            current = q.popleft()
            expanded += 1
            if current == goal:
                return self.reconstruct_path(came_from, start, goal), expanded
            for nxt in self.safe_neighbors(current, blocked):
                if nxt not in visited:
                    visited.add(nxt)
                    came_from[nxt] = current
                    q.append(nxt)
        return [], expanded

    def dfs(self, start, goal, blocked):
        stack = [start]
        came_from = {}
        visited = {start}
        expanded = 0

        while stack:
            current = stack.pop()
            expanded += 1
            if current == goal:
                return self.reconstruct_path(came_from, start, goal), expanded
            for nxt in reversed(self.safe_neighbors(current, blocked)):
                if nxt not in visited:
                    visited.add(nxt)
                    came_from[nxt] = current
                    stack.append(nxt)
        return [], expanded

    def greedy(self, start, goal, blocked):
        heap = []
        heapq.heappush(heap, (self.manhattan(start, goal), start))
        came_from = {}
        visited = {start}
        expanded = 0

        while heap:
            _, current = heapq.heappop(heap)
            expanded += 1
            if current == goal:
                return self.reconstruct_path(came_from, start, goal), expanded
            for nxt in self.safe_neighbors(current, blocked):
                if nxt not in visited:
                    visited.add(nxt)
                    came_from[nxt] = current
                    heapq.heappush(heap, (self.manhattan(nxt, goal), nxt))
        return [], expanded

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

    def flood_fill_space(self, start, blocked):
        if start in blocked or not self.in_bounds(start):
            return 0
        q = deque([start])
        visited = {start}
        count = 0
        while q:
            current = q.popleft()
            count += 1
            for nxt in self.safe_neighbors(current, blocked):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)
        return count

    def choose_fallback_move(self):
        head = self.snake[0]
        body_without_tail = set(self.snake[:-1])
        candidates = []

        for name, (dx, dy) in DIRECTIONS.items():
            if name == OPPOSITE[self.direction] and len(self.snake) > 1:
                continue
            nxt = (head[0] + dx, head[1] + dy)
            if not self.in_bounds(nxt):
                continue
            if nxt in body_without_tail:
                continue
            future_blocked = set(self.snake[:-1])
            open_area = self.flood_fill_space(nxt, future_blocked - {nxt} if nxt in future_blocked else future_blocked)
            food_dist = self.manhattan(nxt, self.food)
            score = (open_area, -food_dist)
            candidates.append((score, name))

        if not candidates:
            return None
        candidates.sort(reverse=True)
        return candidates[0][1]

    def get_ai_move(self):
        start_time = time.perf_counter()
        head = self.snake[0]
        blocked = set(self.snake[:-1])
        algo = self.mode

        if algo == "bfs":
            path, expanded = self.bfs(head, self.food, blocked)
        elif algo == "dfs":
            path, expanded = self.dfs(head, self.food, blocked)
        elif algo == "greedy":
            path, expanded = self.greedy(head, self.food, blocked)
        else:
            path, expanded = self.astar(head, self.food, blocked)

        self.metrics.nodes_expanded = expanded
        self.metrics.last_path_length = max(0, len(path) - 1)
        self.metrics.computation_ms = (time.perf_counter() - start_time) * 1000
        self.cached_path = path

        if len(path) >= 2:
            nxt = path[1]
            move = (nxt[0] - head[0], nxt[1] - head[1])
            for name, vec in DIRECTIONS.items():
                if vec == move:
                    return name

        fallback = self.choose_fallback_move()
        if fallback is not None:
            self.last_reason = "fallback-safe-move"
            return fallback

        self.last_reason = "no-safe-move"
        return self.direction

    def step(self):
        if self.game_over:
            return

        if self.mode != "human":
            self.next_direction = self.get_ai_move()

        if self.next_direction != OPPOSITE[self.direction] or len(self.snake) == 1:
            self.direction = self.next_direction

        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        if not self.in_bounds(new_head):
            self.game_over = True
            self.last_reason = "hit-wall"
            return

        will_grow = new_head == self.food
        body_to_check = self.snake if will_grow else self.snake[:-1]
        if new_head in body_to_check:
            self.game_over = True
            self.last_reason = "hit-self"
            return

        self.snake.insert(0, new_head)

        if will_grow:
            self.metrics.score += 1
            self.metrics.foods_collected += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.metrics.steps_survived += 1

    def handle_key(self, key):
        if key == pygame.K_UP:
            self.next_direction = "UP"
        elif key == pygame.K_DOWN:
            self.next_direction = "DOWN"
        elif key == pygame.K_LEFT:
            self.next_direction = "LEFT"
        elif key == pygame.K_RIGHT:
            self.next_direction = "RIGHT"
        elif key == pygame.K_h:
            self.reset("human")
        elif key == pygame.K_1:
            self.reset("bfs")
        elif key == pygame.K_2:
            self.reset("dfs")
        elif key == pygame.K_3:
            self.reset("greedy")
        elif key == pygame.K_4:
            self.reset("astar")
        elif key == pygame.K_r:
            self.reset(self.mode)

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
        for y in range(0, GRID_HEIGHT * CELL_SIZE + 1, CELL_SIZE):
            pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

    def draw_path(self):
        if len(self.cached_path) < 2 or self.mode == "human":
            return
        for cell in self.cached_path[1:]:
            rx = cell[0] * CELL_SIZE + 6
            ry = cell[1] * CELL_SIZE + 6
            pygame.draw.rect(screen, PATH_COLOR, (rx, ry, CELL_SIZE - 12, CELL_SIZE - 12), border_radius=6)

    def draw(self):
        screen.fill(BG)
        self.draw_grid()
        self.draw_path()

        food_rect = pygame.Rect(self.food[0] * CELL_SIZE + 3, self.food[1] * CELL_SIZE + 3, CELL_SIZE - 6, CELL_SIZE - 6)
        pygame.draw.rect(screen, FOOD, food_rect, border_radius=8)

        for i, segment in enumerate(self.snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            rect = pygame.Rect(segment[0] * CELL_SIZE + 2, segment[1] * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(screen, color, rect, border_radius=8)

        panel_rect = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, WIDTH, 90)
        pygame.draw.rect(screen, PANEL, panel_rect)

        line1 = f"Mode: {self.mode.upper()}    Score: {self.metrics.score}    Steps: {self.metrics.steps_survived}"
        line2 = f"PathLen: {self.metrics.last_path_length}    Nodes: {self.metrics.nodes_expanded}    Time: {self.metrics.computation_ms:.2f} ms"
        line3 = "H Human | 1 BFS | 2 DFS | 3 Greedy | 4 A* | R Restart | ESC Quit"

        screen.blit(font.render(line1, True, TEXT), (12, GRID_HEIGHT * CELL_SIZE + 10))
        screen.blit(small_font.render(line2, True, SUBTEXT), (12, GRID_HEIGHT * CELL_SIZE + 42))
        screen.blit(small_font.render(line3, True, DANGER), (12, GRID_HEIGHT * CELL_SIZE + 64))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, GRID_HEIGHT * CELL_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            msg = f"GAME OVER - {self.last_reason}"
            sub = "Press R to restart or choose another algorithm"
            msg_surface = font.render(msg, True, TEXT)
            sub_surface = small_font.render(sub, True, TEXT)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(sub_surface, (WIDTH // 2 - sub_surface.get_width() // 2, HEIGHT // 2 - 10))

        pygame.display.flip()


def main():
    game = SnakeGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game.handle_key(event.key)

        game.step()
        game.draw()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
