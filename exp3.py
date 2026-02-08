N = 4
board = [-1] * N

def is_safe(row, col):
    for i in range(row):
        # Check same column
        if board[i] == col:
            return False
        # Check diagonal
        if abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve(row):
    if row == N:
        return True

    for col in range(N):
        if is_safe(row, col):
            board[row] = col      # PLACE QUEEN
            if solve(row + 1):
                return True
            board[row] = -1       # BACKTRACK

    return False

solve(0)

# Print the board
for i in range(N):
    print("." * board[i] + "Q" + "." * (N - board[i] - 1))
