from collections import defaultdict, Counter
from typing import List, Tuple, Optional


# -----------------------------
# FP-Tree Node
# -----------------------------

class FPNode:
    def __init__(self, item: Optional[str], parent: Optional["FPNode"]):
        self.item = item
        self.count = 1
        self.parent = parent
        self.children = {}  # item -> FPNode

    def increment(self, n: int = 1):
        self.count += n

    def __repr__(self):
        return f"FPNode(item={self.item}, count={self.count})"


# -----------------------------
# Build FP-Tree
# -----------------------------

def build_fptree(transactions: List[List[str]], min_support: int):
    # Count item frequency (absolute counts)
    freq = Counter()
    for t in transactions:
        for item in t:
            freq[item] += 1

    # Remove infrequent items
    freq = {item: c for item, c in freq.items() if c >= min_support}

    if not freq:
        return None, None

    # Sort items in a transaction by global frequency (descending)
    def sort_items(transaction: List[str]):
        return [
            item
            for item in sorted(transaction, key=lambda x: (-freq.get(x, 0), x))
            if item in freq
        ]

    # Create FP-tree root and header table
    root = FPNode(None, None)
    header = defaultdict(list)  # item -> list of nodes

    # Insert transactions into FP-tree
    for transaction in transactions:
        items = sort_items(transaction)
        current = root

        for item in items:
            if item not in current.children:
                new_node = FPNode(item, current)
                current.children[item] = new_node
                header[item].append(new_node)
            else:
                current.children[item].increment()

            current = current.children[item]

    return root, header


# -----------------------------
# FP-Growth Mining
# -----------------------------

def mine_fp_tree(header: dict,
                 min_support: int,
                 prefix: List[str],
                 frequent_patterns: List[Tuple[List[str], int]]):

    # Iterate items in ascending frequency order (least frequent first)
    items = sorted(
        header.keys(),
        key=lambda it: sum(node.count for node in header[it])
    )

    for item in items:
        new_pattern = prefix + [item]

        # Support of the pattern
        support = sum(node.count for node in header[item])
        frequent_patterns.append((new_pattern, support))

        # Build conditional pattern base (list of prefix paths)
        conditional_base = []

        for node in header[item]:
            path = []
            parent = node.parent

            while parent is not None and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent

            if path:
                for _ in range(node.count):
                    conditional_base.append(list(reversed(path)))

        # Build conditional FP-tree and recurse
        cond_tree, cond_header = build_fptree(conditional_base, min_support)

        if cond_tree is not None and cond_header:
            mine_fp_tree(cond_header, min_support, new_pattern, frequent_patterns)


# -----------------------------
# MAIN FUNCTION: FP-GROWTH
# -----------------------------

def fp_growth(transactions: List[List[str]], min_support: int):
    root, header = build_fptree(transactions, min_support)

    frequent_patterns: List[Tuple[List[str], int]] = []

    if header:
        mine_fp_tree(header, min_support, [], frequent_patterns)

    return frequent_patterns


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    transactions = [
        ["Milk", "Bread", "Beer"],
        ["Milk", "Bread"],
        ["Bread", "Beer"],
        ["Milk", "Beer"],
        ["Milk", "Bread", "Beer"],
    ]

    min_support = 2  # absolute count (transactions appearing at least twice)

    patterns = fp_growth(transactions, min_support)

    print("Frequent Patterns (pattern, support):")

    # Sort for neat output
    for pattern, sup in sorted(patterns, key=lambda x: (-len(x[0]), -x[1], x[0])):
        print(f"{pattern}  support={sup}")