grid = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]
start = (0, 0)
goal = (3, 3)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
open_list = []
closed_list = []
open_list.append((start[0], start[1], 0, None))
while len(open_list) > 0:
    current_index = 0
    for i in range(len(open_list)):
        if open_list[i][2] < open_list[current_index][2]:
            current_index = i
    current = open_list.pop(current_index)
    closed_list.append(current)
    row = current[0]
    col = current[1]
    cost = current[2]
    if (row, col) == goal:
        break
    for move in moves:
        new_row = row + move[0]
        new_col = col + move[1]
        if new_row < 0 or new_row >= 4 or new_col < 0 or new_col >= 4:
            continue
        if grid[new_row][new_col] == 1:
            continue
        visited = False
        for c in closed_list:
            if c[0] == new_row and c[1] == new_col:
                visited = True
                break
        if visited:
            continue
        open_list.append((new_row, new_col, cost + 1, current))
path = []
node = None
for c in closed_list:
    if c[0] == goal[0] and c[1] == goal[1]:
        node = c
        break
while node is not None:
    path.append((node[0], node[1]))
    node = node[3]
path.reverse()
print("Grid:")
for row in grid:
    print(row)
print("\nShortest Path found by A*:")
print(path)