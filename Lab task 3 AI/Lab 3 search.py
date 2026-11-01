# lab3_search.py
# Lab 3, Task 1 - BFS and DFS on the A to G graph, with a printed trace.
# Run with:  python lab3_search.py
#
# Start is A and goal is G. Successors are taken in the listed order.
# A node counts as visited when it is taken out of the queue or stack,
# and the goal is included in the visit order.

from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": [],
}


def bfs(start, goal):
    queue = deque([(start, [start])])
    seen = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            print("  processed", node, "(goal)")
            return path, order
        for n in graph[node]:
            if n not in seen:
                seen.add(n)
                queue.append((n, path + [n]))
        print("  processed", node, "| queue:", [item[0] for item in queue])
    return None, order


def dfs(start, goal):
    stack = [(start, [start])]
    seen = set()
    order = []
    while stack:
        node, path = stack.pop()
        if node in seen:
            continue
        order.append(node)
        if node == goal:
            print("  processed", node, "(goal)")
            return path, order
        seen.add(node)
        # pushed in reverse so the first listed neighbour is popped first
        for n in reversed(graph[node]):
            stack.append((n, path + [n]))
        print("  processed", node, "| stack (top is last):",
              [item[0] for item in stack])
    return None, order


print("BFS")
path, order = bfs("A", "G")
print("path :", path)
print("order:", order)

print()
print("DFS")
path, order = dfs("A", "G")
print("path :", path)
print("order:", order)
