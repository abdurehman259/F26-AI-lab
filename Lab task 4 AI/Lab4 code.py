"""Lab 4: Informed Search, A* audit on the campus graph.

Runs A* with the supplied heuristic, a UCS control (zero heuristic),
an overestimate experiment, and edge case tests.

Queue tie breaking: lowest f, then lowest g, then node name (alphabetical).
Expansion count: a node counts only when its successors are examined.
The goal is logged as processed but is not counted as expanded.
Stale queue entries are skipped and counted separately.
"""

import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Graph = Dict[str, List[Tuple[str, float]]]
Heuristic = Dict[str, float]

INF = float("inf")

CAMPUS_GRAPH: Graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": [],
}
CAMPUS_H: Heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}
START, GOAL = "S", "G"


@dataclass
class Step:
    """State recorded when a node is expanded."""
    node: str
    g: float
    h: float
    f: float
    frontier: List[Tuple[str, float, float]]  # (node, g, f) of live entries


@dataclass
class SearchResult:
    cost: Optional[float] = None
    path: Optional[List[str]] = None
    processed: List[str] = field(default_factory=list)
    expanded: List[str] = field(default_factory=list)
    steps: List[Step] = field(default_factory=list)
    stale: int = 0
    pushes: int = 0


def live_frontier(queue, best) -> List[Tuple[str, float, float]]:
    """Return the non stale queue entries in pop order."""
    return [(n, g, f) for f, g, n, _ in sorted(queue) if g == best[n]]


def astar(graph: Graph, h: Heuristic, start: str, goal: str) -> SearchResult:
    """A* graph search. With h equal to zero everywhere it behaves as UCS."""
    result = SearchResult()
    best = {start: 0}
    queue = [(h[start], 0, start, [start])]
    result.pushes = 1

    while queue:
        f, g, node, path = heapq.heappop(queue)
        if g > best[node]:
            result.stale += 1
            continue
        result.processed.append(node)
        if node == goal:
            result.cost, result.path = g, path
            return result

        result.expanded.append(node)
        for nxt, weight in graph.get(node, []):
            new_g = g + weight
            if new_g < best.get(nxt, INF):
                best[nxt] = new_g
                heapq.heappush(queue, (new_g + h[nxt], new_g, nxt, path + [nxt]))
                result.pushes += 1
        result.steps.append(
            Step(node, g, h[node], f, live_frontier(queue, best))
        )
    return result


def path_cost(graph: Graph, path: List[str]) -> float:
    """Sum edge weights along a path, independent of the search code."""
    total = 0
    for a, b in zip(path, path[1:]):
        weights = [w for n, w in graph.get(a, []) if n == b]
        if not weights:
            raise ValueError(f"No edge from {a} to {b}")
        total += min(weights)
    return total


def true_remaining_costs(graph: Graph, goal: str) -> Dict[str, float]:
    """Exact cost to the goal from every node (Dijkstra on reversed edges)."""
    reverse: Graph = {n: [] for n in graph}
    for u, edges in graph.items():
        for v, w in edges:
            reverse.setdefault(v, []).append((u, w))
    dist = {n: INF for n in reverse}
    dist[goal] = 0
    queue = [(0, goal)]
    while queue:
        d, node = heapq.heappop(queue)
        if d > dist[node]:
            continue
        for prev, w in reverse[node]:
            if d + w < dist[prev]:
                dist[prev] = d + w
                heapq.heappush(queue, (d + w, prev))
    return dist


def audit_heuristic(graph: Graph, h: Heuristic, goal: str):
    """Check admissibility per node and consistency per directed edge."""
    true_cost = true_remaining_costs(graph, goal)
    admissible = [(n, true_cost[n], h[n], h[n] <= true_cost[n]) for n in graph]
    consistent = [
        (u, v, h[u], w + h[v], h[u] <= w + h[v])
        for u, edges in graph.items()
        for v, w in edges
    ]
    return admissible, consistent


def fmt_path(path: Optional[List[str]]) -> str:
    return " to ".join(path) if path else "no path"


def print_run(title: str, graph: Graph, result: SearchResult) -> None:
    print(f"{title}")
    print(f"  Path            : {fmt_path(result.path)}")
    print(f"  Returned cost   : {result.cost}")
    if result.path:
        print(f"  Summed cost     : {path_cost(graph, result.path)}")
    print(f"  Processed order : {', '.join(result.processed)}")
    print(f"  Expanded nodes  : {', '.join(result.expanded)}")
    print(f"  Expansion count : {len(result.expanded)}")
    print(f"  Stale entries   : {result.stale}")
    print(f"  Queue pushes    : {result.pushes}")


def print_manual_trace(result: SearchResult, limit: int = 3) -> None:
    for i, s in enumerate(result.steps[:limit], start=1):
        print(f"  Expansion {i}: node {s.node}, g={s.g}, h={s.h}, f={s.f}")
        entries = ", ".join(f"{n}(g={g}, f={f})" for n, g, f in s.frontier)
        print(f"    Frontier after expansion: {entries or 'empty'}")


def main() -> None:
    zero_h = {n: 0 for n in CAMPUS_H}

    print("TASK 1: Heuristic audit and manual trace")
    admissible, consistent = audit_heuristic(CAMPUS_GRAPH, CAMPUS_H, GOAL)
    for n, true_c, hv, ok in admissible:
        print(f"  Node {n}: true={true_c}, h={hv}, admissible={ok}")
    for u, v, hu, rhs, ok in consistent:
        print(f"  Edge {u} to {v}: h(u)={hu}, cost+h(v)={rhs}, consistent={ok}")
    astar_run = astar(CAMPUS_GRAPH, CAMPUS_H, START, GOAL)
    print_manual_trace(astar_run)

    print("\nTASK 2: A* versus UCS")
    ucs_run = astar(CAMPUS_GRAPH, zero_h, START, GOAL)
    print_run("A* (supplied heuristic)", CAMPUS_GRAPH, astar_run)
    print_run("UCS (zero heuristic)", CAMPUS_GRAPH, ucs_run)
    assert astar_run.cost == path_cost(CAMPUS_GRAPH, astar_run.path)
    assert ucs_run.cost == path_cost(CAMPUS_GRAPH, ucs_run.path)
    assert astar_run.cost == ucs_run.cost == 6

    print("\nTASK 3: Overestimate experiment")
    over_h = dict(CAMPUS_H, C=10)
    over_run = astar(CAMPUS_GRAPH, over_h, START, GOAL)
    print("  h(C) changed from 2 to 10, true remaining cost of C is 3")
    print_run("A* with h(C)=10", CAMPUS_GRAPH, over_run)
    print_manual_trace(over_run)

    mild_h = dict(CAMPUS_H, C=4)
    mild_run = astar(CAMPUS_GRAPH, mild_h, START, GOAL)
    print("  Extra run: h(C)=4 also overestimates but the answer is unchanged")
    print_run("A* with h(C)=4", CAMPUS_GRAPH, mild_run)

    print("\nEDGE CASES")
    start_is_goal = astar(CAMPUS_GRAPH, CAMPUS_H, "G", "G")
    print_run("Start equals goal", CAMPUS_GRAPH, start_is_goal)

    cut_graph = dict(CAMPUS_GRAPH, D=[])
    cut_h = dict(CAMPUS_H, D=0)
    unreachable = astar(cut_graph, cut_h, START, "D")
    print_run("Unreachable goal D", cut_graph, unreachable)

    stale_graph: Graph = {
        "S": [("A", 4), ("B", 1)],
        "B": [("A", 1)],
        "A": [("G", 5)],
        "G": [],
    }
    stale_h = {n: 0 for n in stale_graph}
    stale_run = astar(stale_graph, stale_h, START, GOAL)
    print_run("Stale entry case (better path to A found later)",
              stale_graph, stale_run)


if __name__ == "__main__":
    main()
