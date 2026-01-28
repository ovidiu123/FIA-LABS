# run_task2.py
import numpy as np

from maze import generate_random_solvable_maze
from search import bfs, astar
from simulation import Robot, MultiRobotSimulator

def main():
    height, width = 35, 35
    start = (1, 1)
    goal = (height - 2, width - 2)

    # 1) Generate solvable maze using BFS as validator
    maze = generate_random_solvable_maze(
        height=height,
        width=width,
        wall_prob=0.28,
        start=start,
        goal=goal,
        solver_fn=bfs,
        rng_seed=42
    )

    # 2) Solve with BFS °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    bfs_path, bfs_meta = bfs(maze, start, goal)

    # 3) Solve with A* °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    a_path, a_meta = astar(maze, start, goal)

    print("=== RESULTS ===")
    print(bfs_meta)
    print(a_meta)

    # Show paths °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    maze.draw(start=start, goal=goal, path=bfs_path, title=f"BFS path length = {bfs_meta.path_length}, explored = {bfs_meta.explored_nodes}")
    maze.draw(start=start, goal=goal, path=a_path, title=f"A* path length = {a_meta.path_length}, explored = {a_meta.explored_nodes}")

    # 4) Optional: multi-robot fairness demo °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
    robots = [
        Robot(pos=(1, 1), goal=(height - 2, width - 2)),
        Robot(pos=(1, width - 2), goal=(height - 2, 1)),
        Robot(pos=(height - 2, 1), goal=(1, width - 2)),
    ]
    sim = MultiRobotSimulator(maze, robots)
    ticks = sim.run(max_ticks=1000)

    print(f"\nMulti-robot finished in {ticks} ticks.")
    maze.draw(robots=[r.pos for r in robots], title="Final robot positions (round-robin fairness)")

if __name__ == "__main__":
    main()
