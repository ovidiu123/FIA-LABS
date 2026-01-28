# simulation.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

from maze import GridMaze, Coord
from search import astar

@dataclass
class Robot:
    pos: Coord
    goal: Coord
    path: Optional[List[Coord]] = None
    done: bool = False


class MultiRobotSimulator:

    def __init__(self, maze: GridMaze, robots: List[Robot]):
        self.maze = maze
        self.robots = robots
        self.tick = 0

    def occupied(self) -> set[Coord]:
        return {r.pos for r in self.robots}

    def plan_for_robot(self, i: int) -> None:
        r = self.robots[i]
        if r.done:
            return
        path, _meta = astar(self.maze, r.pos, r.goal)
        r.path = path

    def step(self) -> None:
        self.tick += 1
        occ = self.occupied()

        # Round-robin order shifts each tick
        n = len(self.robots)
        order = [(self.tick + k) % n for k in range(n)]

        for i in order:
            rob = self.robots[i]
            if rob.done:
                continue

            # If already at goal °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
            if rob.pos == rob.goal:
                rob.done = True
                continue

            # Plan if no path °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
            if not rob.path or len(rob.path) < 2:
                self.plan_for_robot(i)

            if not rob.path or len(rob.path) < 2:
                # no path found (shouldn't happen in solvable maze unless other robots block) °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
                continue

            nxt = rob.path[1]  # next step after current °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･

            # collision check °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
            if nxt in occ:
                # blocked -> try replan once
                self.plan_for_robot(i)
                if rob.path and len(rob.path) >= 2:
                    nxt = rob.path[1]
                    if nxt in occ:
                        continue  # still blocked -> wait °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
                else:
                    continue

            # Move °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
            occ.remove(rob.pos)
            rob.pos = nxt
            occ.add(rob.pos)

            # Remove consumed step from path °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
            rob.path = rob.path[1:]

            if rob.pos == rob.goal:
                rob.done = True

    def run(self, max_ticks: int = 500) -> int:
        for _ in range(max_ticks):
            if all(r.done for r in self.robots):
                break
            self.step()
        return self.tick
