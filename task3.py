from __future__ import annotations
import random
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt


Node = int
Color = str


# ---------------------------
# Utility / Validation
# ---------------------------

def is_valid_coloring(adj: Dict[Node, Set[Node]], assignment: Dict[Node, Color]) -> bool:
    for u, nbs in adj.items():
        if u not in assignment:
            continue
        for v in nbs:
            if v in assignment and assignment[v] == assignment[u]:
                return False
    return True


def count_edges(adj: Dict[Node, Set[Node]]) -> int:
    return sum(len(nbs) for nbs in adj.values()) // 2


# ---------------------------
# Random "map" generator (graph) °❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･°❀⋆.ೃ࿔*:･
# ---------------------------

def generate_random_graph(n: int, p: float, seed: int) -> Dict[Node, Set[Node]]:
    """
    Generates an undirected random graph as a stand-in for a "map".
    For the lab it's acceptable unless they explicitly demand planar maps.
    """
    rng = random.Random(seed)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i].add(j)
                adj[j].add(i)
    return adj


# ---------------------------
# CSP Solver (Backtracking + Domain Reduction)
# ---------------------------

def select_unassigned_var(adj: Dict[Node, Set[Node]],
                          domains: Dict[Node, Set[Color]],
                          assignment: Dict[Node, Color]) -> Node:
    """
    MRV heuristic: choose the unassigned node with the smallest remaining domain.
    Tie-breaker: higher degree first.
    """
    unassigned = [v for v in adj.keys() if v not in assignment]
    # Minimum Remaining Values
    best_size = min(len(domains[v]) for v in unassigned)
    candidates = [v for v in unassigned if len(domains[v]) == best_size]
    # Degree tie-break
    return max(candidates, key=lambda v: len(adj[v]))


def order_values_lcv(adj: Dict[Node, Set[Node]],
                     var: Node,
                     domains: Dict[Node, Set[Color]],
                     assignment: Dict[Node, Color]) -> List[Color]:
    """
    Least Constraining Value: prefer colors that eliminate fewer options for neighbors.
    (Optional but helps performance, still easy to explain.)
    """
    def impact(color: Color) -> int:
        eliminated = 0
        for nb in adj[var]:
            if nb not in assignment and color in domains[nb]:
                eliminated += 1
        return eliminated

    return sorted(domains[var], key=impact)


def forward_check(adj: Dict[Node, Set[Node]],
                  var: Node,
                  color: Color,
                  domains: Dict[Node, Set[Color]],
                  assignment: Dict[Node, Color]) -> Tuple[bool, Dict[Node, Set[Color]]]:
    """
    Domain reduction (forward checking):
    After assigning var=color, remove 'color' from each neighbor's domain.
    If any neighbor domain becomes empty -> failure.
    """
    new_domains = {v: set(domains[v]) for v in domains}
    new_domains[var] = {color}

    for nb in adj[var]:
        if nb in assignment:
            if assignment[nb] == color:
                return False, domains
        else:
            if color in new_domains[nb]:
                new_domains[nb].remove(color)
                if len(new_domains[nb]) == 0:
                    return False, domains

    return True, new_domains


def solve_map_coloring(adj: Dict[Node, Set[Node]], colors: List[Color], seed: int = 0) -> Optional[Dict[Node, Color]]:
    """
    Backtracking CSP solver with:
    - MRV variable selection
    - forward checking (domain reduction)
    - optional LCV ordering
    """
    rng = random.Random(seed)
    domains: Dict[Node, Set[Color]] = {v: set(colors) for v in adj}
    assignment: Dict[Node, Color] = {}

    # simple counters (for report)
    stats = {"calls": 0, "fails": 0}

    def backtrack(domains: Dict[Node, Set[Color]]) -> Optional[Dict[Node, Color]]:
        stats["calls"] += 1

        if len(assignment) == len(adj):
            return dict(assignment)

        var = select_unassigned_var(adj, domains, assignment)
        values = order_values_lcv(adj, var, domains, assignment)

        # (Tiny randomness can prevent worst-case loops, but keep it simple)
        # rng.shuffle(values)

        for color in values:
            # local consistency check
            if any(assignment.get(nb) == color for nb in adj[var]):
                continue

            ok, new_domains = forward_check(adj, var, color, domains, assignment)
            if not ok:
                continue

            assignment[var] = color
            res = backtrack(new_domains)
            if res is not None:
                return res
            del assignment[var]

        stats["fails"] += 1
        return None

    sol = backtrack(domains)
    # attach stats to solution for printing
    if sol is not None:
        sol["_stats_calls"] = stats["calls"]
        sol["_stats_fails"] = stats["fails"]
    return sol


# ---------------------------
# Generate random SOLVABLE test maps
# ---------------------------

def generate_random_solvable_map(n: int = 18,
                                 p: float = 0.22,
                                 k: int = 4,
                                 seed: int = 42,
                                 max_tries: int = 300) -> Tuple[Dict[Node, Set[Node]], Dict[Node, Color], List[Color]]:
    """
    Re-generate random graphs until solvable with k colors.
    """
    colors = [f"C{i+1}" for i in range(k)]

    for t in range(max_tries):
        adj = generate_random_graph(n=n, p=p, seed=seed + t)
        sol = solve_map_coloring(adj, colors, seed=seed + t)
        if sol is None:
            continue

        # Remove stats keys for validation
        stats_calls = sol.pop("_stats_calls", None)
        stats_fails = sol.pop("_stats_fails", None)

        if is_valid_coloring(adj, sol):
            # put stats back in a separate dict for reporting if needed
            sol["_stats_calls"] = stats_calls
            sol["_stats_fails"] = stats_fails
            return adj, sol, colors

    raise RuntimeError("Could not generate solvable map. Try increasing k or lowering p.")


# ---------------------------
# Visualization (optional)
# ---------------------------

def plot_graph_coloring(adj: Dict[Node, Set[Node]], assignment: Dict[Node, Color], title: str = "") -> None:
    """
    Simple visualization using random 2D positions (not a true geographic map, but clear for demo).
    """
    nodes = list(adj.keys())
    n = len(nodes)
    rng = np.random.default_rng(0)
    pos = rng.random((n, 2))

    # map colors to integers for plotting
    unique_colors = sorted({assignment[v] for v in nodes if v in assignment})
    color_to_id = {c: i for i, c in enumerate(unique_colors)}
    node_colors = [color_to_id.get(assignment.get(v, unique_colors[0]), 0) for v in nodes]

    plt.figure(figsize=(7, 6))
    # edges
    for u in nodes:
        for v in adj[u]:
            if u < v:
                x = [pos[u, 0], pos[v, 0]]
                y = [pos[u, 1], pos[v, 1]]
                plt.plot(x, y, linewidth=1)

    # nodes
    plt.scatter(pos[:, 0], pos[:, 1], s=250, c=node_colors)

    # labels
    for i in nodes:
        plt.text(pos[i, 0], pos[i, 1], str(i), ha="center", va="center", fontsize=10)

    if title:
        plt.title(title)
    plt.xticks([])
    plt.yticks([])
    plt.show()


# ---------------------------
# Main demo
# ---------------------------

def main():
    # Tweak these if needed
    N_DISTRICTS = 18
    EDGE_PROB = 0.22
    K_COLORS = 4

    adj, sol, colors = generate_random_solvable_map(n=N_DISTRICTS, p=EDGE_PROB, k=K_COLORS, seed=7)

    calls = sol.pop("_stats_calls", None)
    fails = sol.pop("_stats_fails", None)

    print("=== TASK 3: MAP COLORING CSP ===")
    print(f"Districts: {N_DISTRICTS}")
    print(f"Edges: {count_edges(adj)} (p={EDGE_PROB})")
    print(f"Colors: {colors}")
    print(f"Solved: {is_valid_coloring(adj, sol)}")
    if calls is not None:
        print(f"Backtracking calls: {calls}, dead-ends: {fails}")

    # Print solution nicely
    for v in sorted(sol.keys()):
        print(f"District {v:02d} -> {sol[v]}")

    plot_graph_coloring(adj, sol, title="Random solvable map coloring (CSP + forward checking)")


if __name__ == "__main__":
    main()
