from collections import deque
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['D', 'G'],
    'D': ['B', 'F'],
    'E': [],
    'F': ['G', 'H'],
    'G': [],
    'H': []
}
def bfs_shortest_path(start, goal):
    q = deque([(start, [start])])
    visited = set()

    while q:
        node, path = q.popleft()

        if node == goal:
            return path

        visited.add(node)

        for child in graph[node]:
            if child not in visited:
                q.append((child, path + [child]))

    return None
def dfs_path(start, goal, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == goal:
        return path
    for child in graph[start]:
        if child not in visited:
            result = dfs_path(child, goal, visited, path)
            if result:
                return result
    path.pop()
    return None
start = input("Start node: ")
goal = input("Goal node: ")
bfs_path_result = bfs_shortest_path(start, goal)
dfs_path_result = dfs_path(start, goal)
print("\nShortest Path (BFS):", "->".join(bfs_path_result))
print("Path (DFS):", "->".join(dfs_path_result))