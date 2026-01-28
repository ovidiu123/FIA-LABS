# maze.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt

Coord = Tuple[int, int]  # (row, col)

@dataclass
class GridMaze:
    grid: np.ndarray  # 0 = free, 1 = wall °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･

    @property
    def h(self) -> int:
        return self.grid.shape[0]

    @property
    def w(self) -> int:
        return self.grid.shape[1]

    def in_bounds(self, p: Coord) -> bool:
        r, c = p
        return 0 <= r < self.h and 0 <= c < self.w

    def passable(self, p: Coord) -> bool:
        r, c = p
        return self.grid[r, c] == 0

    def neighbors4(self, p: Coord) -> List[Coord]:
        r, c = p
        cand = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        return [q for q in cand if self.in_bounds(q) and self.passable(q)]

    def draw(self, start: Optional[Coord] = None, goal: Optional[Coord] = None,
             path: Optional[List[Coord]] = None, robots: Optional[List[Coord]] = None,
             title: str = "") -> None:
        img = self.grid.copy()

        plt.figure(figsize=(7, 7))
        plt.imshow(img, interpolation="nearest")
        plt.xticks([])
        plt.yticks([])
        if title:
            plt.title(title)

        # Path °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
        if path:
            pr = [p[0] for p in path]
            pc = [p[1] for p in path]
            plt.plot(pc, pr, linewidth=2)

        # Start/goal
        if start is not None:
            plt.scatter([start[1]], [start[0]], s=120, marker="o")
        if goal is not None:
            plt.scatter([goal[1]], [goal[0]], s=120, marker="X")

        # Robots °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
        if robots:
            rr = [p[0] for p in robots]
            rc = [p[1] for p in robots]
            plt.scatter(rc, rr, s=120, marker="s")

        plt.show()


def generate_random_solvable_maze(
    height: int,
    width: int,
    wall_prob: float,
    start: Coord,
    goal: Coord,
    solver_fn,                 # e.g. BFS or A* to validate solvable °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･ °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    max_tries: int = 10_000,
    rng_seed: int = 42
) -> GridMaze:
    """
    randomly generates walls until there exists a path from start to goal °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.
    """
    rng = np.random.default_rng(rng_seed)

    for _ in range(max_tries):
        grid = (rng.random((height, width)) < wall_prob).astype(np.int8)

        # Ensure borders can remain random; but guarantee start/goal free:
        grid[start[0], start[1]] = 0
        grid[goal[0], goal[1]] = 0

        maze = GridMaze(grid)

        path, meta = solver_fn(maze, start, goal)
        if path is not None and len(path) > 0:
            return maze

    raise RuntimeError("Could not generate a solvable maze within max_tries. Try lower wall_prob.")
