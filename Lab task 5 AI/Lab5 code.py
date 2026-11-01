"""Lab 5: Adversarial Search, Minimax and Alpha Beta Pruning.

The game tree is a complete binary tree stored as a flat list of leaf scores.
The root is a MAX node and levels alternate between MAX and MIN.
A leaf is counted each time its utility is read.
A branch is pruned when alpha is greater than or equal to beta.
Root move 0 is the left child and 1 is the right child. Ties pick the first.
"""

import math
from dataclasses import dataclass, field
from itertools import product
from typing import Iterator, List, Optional

NEG_INF = float("-inf")
POS_INF = float("inf")

TREE_A = [3, 5, 2, 9, 0, 7]      # Minimax tree from the manual, padded below
TREE_B = [3, 5, 2, 9, 3, 5, 2, 9]  # Alpha beta tree from the manual


@dataclass
class Counter:
    """Counts evaluated leaves and records pruning decisions."""
    leaves: int = 0
    prunes: List[str] = field(default_factory=list)


@dataclass
class Decision:
    value: float
    move: Optional[int]
    leaves: int
    prunes: List[str]


def pad_scores(scores: List[float]) -> List[float]:
    """Pad with zeros up to the next power of two, as the manual does."""
    if not scores:
        raise ValueError("scores must not be empty")
    size = 2 ** math.ceil(math.log2(len(scores)))
    return list(scores) + [0] * (size - len(scores))


def tree_depth(scores: List[float]) -> int:
    """Depth of a complete binary tree. Rejects sizes that are not powers of two."""
    size = len(scores)
    if size == 0 or size & (size - 1):
        raise ValueError(f"{size} leaves do not form a complete binary tree")
    return int(math.log2(size))


def minimax(depth: int, index: int, max_turn: bool, scores: List[float],
            target: int, counter: Counter) -> float:
    """Plain Minimax. Every leaf below the node is evaluated."""
    if depth == target:
        counter.leaves += 1
        return scores[index]
    choose = max if max_turn else min
    return choose(
        minimax(depth + 1, index * 2 + i, not max_turn, scores, target, counter)
        for i in range(2)
    )


def alphabeta(depth: int, index: int, max_turn: bool, scores: List[float],
              target: int, alpha: float, beta: float, counter: Counter) -> float:
    """Minimax with alpha beta pruning."""
    if depth == target:
        counter.leaves += 1
        return scores[index]

    value = NEG_INF if max_turn else POS_INF
    for i in range(2):
        child = alphabeta(depth + 1, index * 2 + i, not max_turn, scores,
                          target, alpha, beta, counter)
        if max_turn:
            value = max(value, child)
            alpha = max(alpha, value)
        else:
            value = min(value, child)
            beta = min(beta, value)
        if alpha >= beta:
            if i == 0:
                kind = "MAX" if max_turn else "MIN"
                counter.prunes.append(
                    f"{kind} node at depth {depth}, index {index}: "
                    f"alpha {alpha} and beta {beta}, second child skipped")
            break
    return value


def decide(scores: List[float], use_pruning: bool) -> Decision:
    """Choose the root move and report value and leaf count."""
    target = tree_depth(scores)
    counter = Counter()
    if target == 0:
        counter.leaves = 1
        return Decision(scores[0], None, counter.leaves, counter.prunes)

    best_value, move, alpha = NEG_INF, None, NEG_INF
    for i in range(2):
        if use_pruning:
            value = alphabeta(1, i, False, scores, target, alpha, POS_INF, counter)
        else:
            value = minimax(1, i, False, scores, target, counter)
        if value > best_value:
            best_value, move = value, i
        alpha = max(alpha, best_value)
    return Decision(best_value, move, counter.leaves, counter.prunes)


def arrangements(leaves: List[float]) -> Iterator[List[float]]:
    """Every ordering reachable by swapping the two children of any node."""
    if len(leaves) == 1:
        yield list(leaves)
        return
    half = len(leaves) // 2
    for left, right in product(arrangements(leaves[:half]),
                               arrangements(leaves[half:])):
        yield left + right
        yield right + left


def print_manual_trace(scores: List[float]) -> None:
    """Bottom up Minimax values, level by level."""
    target = tree_depth(scores)
    values = list(scores)
    print(f"  Leaves: {values}")
    for depth in range(target - 1, -1, -1):
        is_max = depth % 2 == 0
        choose = max if is_max else min
        values = [choose(values[i], values[i + 1]) for i in range(0, len(values), 2)]
        print(f"  Depth {depth} ({'MAX' if is_max else 'MIN'}): {values}")


def compare(name: str, scores: List[float]) -> None:
    plain = decide(scores, use_pruning=False)
    pruned = decide(scores, use_pruning=True)
    assert plain.value == pruned.value and plain.move == pruned.move
    assert pruned.leaves <= plain.leaves
    print(f"{name}: {scores}")
    print(f"  Minimax    : value {plain.value}, move {plain.move}, leaves {plain.leaves}")
    print(f"  Alpha beta : value {pruned.value}, move {pruned.move}, leaves {pruned.leaves}")
    for note in pruned.prunes:
        print(f"    Pruned: {note}")


def reorder_experiment(name: str, scores: List[float]) -> None:
    results = [(decide(s, True), s) for s in arrangements(scores)]
    base = decide(scores, False).value
    assert all(r.value == base for r, _ in results), "pruning changed the value"
    best = min(results, key=lambda x: x[0].leaves)
    worst = max(results, key=lambda x: x[0].leaves)
    original = decide(scores, True).leaves
    reverse = decide(scores[::-1], True).leaves
    print(f"{name}: {len(results)} orderings tested, value always {base}")
    print(f"  Original order : {original} leaves")
    print(f"  Reversed order : {reverse} leaves")
    print(f"  Best order     : {best[0].leaves} leaves, {best[1]}")
    print(f"  Worst order    : {worst[0].leaves} leaves, {worst[1]}")


def main() -> None:
    tree_a = pad_scores(TREE_A)

    print("TASK 1: Manual Minimax trace (Tree A, padded)")
    print_manual_trace(tree_a)

    print("\nTASK 2: Leaf counts")
    compare("Tree A", tree_a)
    compare("Tree B", TREE_B)

    print("\nTASK 3: Reordering branches")
    reorder_experiment("Tree A", tree_a)
    reorder_experiment("Tree B", TREE_B)

    print("\nEDGE CASES")
    compare("Single leaf", [7])
    compare("All equal leaves", [4] * 8)
    try:
        tree_depth(TREE_A)
    except ValueError as error:
        print(f"Unpadded Tree A rejected: {error}")


if __name__ == "__main__":
    main()
