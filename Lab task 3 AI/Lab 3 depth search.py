# lab3_depth_search.py
# Lab 3, Task 2 - depth limited search (DLS) on the A to G graph.
# Run with:  python lab3_depth_search.py
#
# The root is at depth 0. The cycle check only looks at the current path,
# so the same node can still be reached through a different branch.
# Results are FOUND, CUTOFF or FAILURE.

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}


def dls(g, node, goal, limit, path):
    """Return (status, path) for a search from node."""
    if node == goal:
        return "FOUND", path

    # children that are not already on this path
    children = [n for n in g[node] if n not in path]

    if limit == 0:
        # out of depth, but is there more below that we did not look at?
        if children:
            return "CUTOFF", None
        return "FAILURE", None

    cutoff = False
    for n in children:
        status, result = dls(g, n, goal, limit - 1, path + [n])
        if status == "FOUND":
            return status, result
        if status == "CUTOFF":
            cutoff = True

    if cutoff:
        return "CUTOFF", None
    return "FAILURE", None


print("DLS from A to G")
for limit in [1, 2, 3, 4]:
    status, path = dls(graph, "A", "G", limit, ["A"])
    print("limit", limit, "|", status, "|", path)

# extra tests
print()
print("extra tests")

status, path = dls(graph, "A", "A", 0, ["A"])
print("start equals goal :", status, path)

cycle_graph = {"A": ["B"], "B": ["A", "C"], "C": []}
status, path = dls(cycle_graph, "A", "G", 5, ["A"])
print("cycle, no goal    :", status, path)
