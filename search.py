from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import heapq
from collections import deque

from maze import GridMaze, Coord

@dataclass
class SearchMeta:
    explored_nodes: int
    path_length: int
    algorithm: str


def reconstruct_path(came_from: Dict[Coord, Optional[Coord]], start: Coord, goal: Coord) -> List[Coord]:
    cur = goal
    path = []
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur, None)
    path.reverse()
    if path and path[0] == start:
        return path
    return []


def bfs(maze: GridMaze, start: Coord, goal: Coord) -> Tuple[Optional[List[Coord]], SearchMeta]:
    q = deque([start])
    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    explored = 0

    while q:
        cur = q.popleft()
        explored += 1

        if cur == goal:
            path = reconstruct_path(came_from, start, goal)
            meta = SearchMeta(explored_nodes=explored, path_length=len(path) - 1, algorithm="BFS")
            return path, meta

        for nxt in maze.neighbors4(cur):
            if nxt not in came_from:
                came_from[nxt] = cur
                q.append(nxt)

    meta = SearchMeta(explored_nodes=explored, path_length=-1, algorithm="BFS")
    return None, meta


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
def astar(maze: GridMaze, start: Coord, goal: Coord) -> Tuple[Optional[List[Coord]], SearchMeta]:
    """
    A* for 4-neighborhood uniform cost grid.
    f(n)=g(n)+h(n) where h = Manhattan distance (admissible).
    """
    open_heap: List[Tuple[int, int, Coord]] = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))

    came_from: Dict[Coord, Optional[Coord]] = {start: None}
    g_cost: Dict[Coord, int] = {start: 0}
    explored = 0

    while open_heap:
        f, g, cur = heapq.heappop(open_heap)
        explored += 1

        if cur == goal:
            path = reconstruct_path(came_from, start, goal)
            meta = SearchMeta(explored_nodes=explored, path_length=len(path) - 1, algorithm="A*")
            return path, meta

        for nxt in maze.neighbors4(cur):
            tentative_g = g_cost[cur] + 1
            if nxt not in g_cost or tentative_g < g_cost[nxt]:
                g_cost[nxt] = tentative_g
                came_from[nxt] = cur
                f_cost = tentative_g + manhattan(nxt, goal)
                heapq.heappush(open_heap, (f_cost, tentative_g, nxt))

    meta = SearchMeta(explored_nodes=explored, path_length=-1, algorithm="A*")
    return None, meta
