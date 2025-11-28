# 8-Puzzle Solver using Depth First Search (DFS)

from collections import deque

# Goal state (you can change if needed)
GOAL_STATE = ((1, 2, 3),
              (8, 0, 4),
              (7, 6, 5))   # 0 = blank

# Function to find blank position
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Function to generate neighbors (Up, Down, Left, Right)
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    moves = [(-1,0), (1,0), (0,-1), (0,1)]  # Up, Down, Left, Right

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [list(row) for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(tuple(tuple(row) for row in new_state))
return neighbors

# Depth First Search
def dfs(start_state, max_depth=20):
    stack = [(start_state, [start_state], 0)]  # (state, path, depth)
    visited = set()

    while stack:
        state, path, depth = stack.pop()

        # Goal test
        if state == GOAL_STATE:
            return path

        # Depth limit check
        if depth >= max_depth:
            continue

        if state in visited:
            continue
        visited.add(state)

        # Expand neighbors
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], depth + 1))

    return None  # No solution found within limit

# Example usage
start_state = ((2, 8, 3),
               (1, 6, 4),
               (7, 0, 5))

solution = dfs(start_state, max_depth=20)

# Print solution
if solution:
    print("✅ Solution found in", len(solution)-1, "moves:\n")
    for step, state in enumerate(solution):
        print("Step", step)
        for row in state:
            print(row)
        print()
else:
    print("❌ No solution found within depth limit.")
✅ Solution found in 19 moves:

Step 0
(2, 8, 3)
(1, 6, 4)
(7, 0, 5)

Step 1
(2, 8, 3)
(1, 6, 4)
(7, 5, 0)

Step 2
(2, 8, 3)
(1, 6, 0)
(7, 5, 4)

Step 3
(2, 8, 3)
(1, 0, 6)
(7, 5, 4)

Step 4
(2, 8, 3)
(1, 5, 6)
(7, 0, 4)
Step 5
(2, 8, 3)
(1, 5, 6)
(7, 4, 0)

Step 6
(2, 8, 3)
(1, 5, 0)
(7, 4, 6)

Step 7
(2, 8, 3)
(1, 0, 5)
(7, 4, 6)

Step 8
(2, 8, 3)
(0, 1, 5)
(7, 4, 6)

Step 9
(0, 8, 3)
(2, 1, 5)
(7, 4, 6)

Step 10
(8, 0, 3)
(2, 1, 5)
(7, 4, 6)

Step 11
(8, 1, 3)
(2, 0, 5)
(7, 4, 6)

Step 12
(8, 1, 3)
(0, 2, 5)
(7, 4, 6)
Step 13
(0, 1, 3)
(8, 2, 5)
(7, 4, 6)

Step 14
(1, 0, 3)
(8, 2, 5)
(7, 4, 6)

Step 15
(1, 2, 3)
(8, 0, 5)
(7, 4, 6)

Step 16
(1, 2, 3)
(8, 4, 5)
(7, 0, 6)

Step 17
(1, 2, 3)
(8, 4, 5)
(7, 6, 0)

Step 18
(1, 2, 3)
(8, 4, 0)
(7, 6, 5)

Step 19
(1, 2, 3)
(8, 0, 4)
(7, 6, 5)
