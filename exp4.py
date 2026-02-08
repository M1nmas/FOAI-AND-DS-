def alphabeta(node, depth, alpha, beta, maximizingPlayer, tree):
    if depth == 0 or node not in tree:
        return node
    if maximizingPlayer:
        maxEval = -9999
        for child in tree[node]:
            eval = alphabeta(child, depth - 1, alpha, beta, False, tree)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 9999
        for child in tree[node]:
            eval = alphabeta(child, depth - 1, alpha, beta, True, tree)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
game_tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [3, 5],
    'E': [6, 9],
    'F': [1, 2],
    'G': [0, -1]
}
leaf_tree = {}
for k, v in game_tree.items():
    leaf_tree[k] = v
print("Optimal value using Alpha-Beta Pruning:")
result = alphabeta('A', 3, -9999, 9999, True, leaf_tree)
print("Result =", result)