import random

def calculate_cost(board):
    """Count number of attacking queen pairs."""
    cost = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                cost += 1
    return cost


def get_neighbors(board):
    """Generate neighbors by moving each queen to another row."""
    neighbors = []
    n = len(board)
    for col in range(n):
        for new_row in range(n):
            if new_row != board[col]:
                new_board = board[:]
                new_board[col] = new_row
                neighbors.append(new_board)
    return neighbors


def hill_climbing(n, max_restarts=100):
    """Perform hill climbing with random restarts."""
    solutions = set()
    all_iterations = []

    for restart in range(max_restarts):

        # Random initial board
        current_board = [random.randint(0, n - 1) for _ in range(n)]
        current_cost = calculate_cost(current_board)

        iterations = []
        iterations.append((list(current_board), current_cost))

        # Hill Climbing Loop
        while current_cost > 0:
            neighbors = get_neighbors(current_board)
            next_board = None
            next_cost = current_cost

            for neighbor in neighbors:
                cost = calculate_cost(neighbor)
                if cost < next_cost:
                    next_board = neighbor
                    next_cost = cost

            if next_board is None:
                break  # Local optimum reached

            current_board = next_board
            current_cost = next_cost
            iterations.append((list(current_board), current_cost))

        if current_cost == 0:
            solutions.add(tuple(current_board))

        all_iterations.append(iterations)

    return list(solutions), all_iterations


def print_solution(board):
    print(" ".join(map(str, board)))




n = 4
solutions, all_iterations = hill_climbing(n)

print("Name: Prakrithi")
print("USN: 1BM23CS239\n")

# Print all restarts & iterations
for restart_idx, iterations in enumerate(all_iterations):
    print(f"Restart {restart_idx + 1}:")
    for step_idx, (board_state, cost) in enumerate(iterations):
        print(f"Iteration {step_idx + 1}:")
        print_solution(board_state)
        print(f"Cost: {cost}\n")

# Print all found solutions
for i, solution in enumerate(solutions):
    print(f"Solution {i + 1}:")
    print_solution(solution)
    print()

Name: Prakrithi
USN: 1BM23CS239

Restart 1:
Iteration 1:
0 3 0 3
Cost: 3

Iteration 2:
1 3 0 3
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 2:
Iteration 1:
0 3 1 2
Cost: 1

Restart 3:
Iteration 1:
2 3 3 1
Cost: 3

Iteration 2:
2 0 3 1
Cost: 0

Restart 4:
Iteration 1:
3 0 0 2
Cost: 2

Iteration 2:
3 1 0 2
Cost: 1

Restart 5:
Iteration 1:
2 1 0 0
Cost: 4

Iteration 2:
2 1 3 0
Cost: 1

Restart 6:
Iteration 1:
0 3 1 1
Cost: 2

Iteration 2:
0 3 1 2
Cost: 1

Restart 7:
Iteration 1:
2 2 2 1
Cost: 4

Iteration 2:
2 0 2 1
Cost: 2

Iteration 3:
2 0 3 1
Cost: 0

Restart 8:
Iteration 1:
1 0 0 3
Cost: 2

Iteration 2:
1 2 0 3
Cost: 1

Restart 9:
Iteration 1:
1 0 2 3
Cost: 2

Restart 10:
Iteration 1:
1 0 3 2
Cost: 4

Iteration 2:
0 0 3 2
Cost: 3

Iteration 3:
0 0 3 1
Cost: 1

Iteration 4:
2 0 3 1
Cost: 0

Restart 11:
Iteration 1:
3 3 1 0
Cost: 4

Iteration 2:
0 3 1 0
Cost: 2

Iteration 3:
0 3 1 2
Cost: 1

Restart 12:
Iteration 1:
3 2 2 1
Cost: 3

Iteration 2:
3 0 2 1
Cost: 1

Restart 13:
Iteration 1:
3 3 2 3
Cost: 5

Iteration 2:
3 0 2 3
Cost: 2

Iteration 3:
3 0 2 1
Cost: 1

Restart 14:
Iteration 1:
1 1 2 2
Cost: 3

Iteration 2:
3 1 2 2
Cost: 2

Iteration 3:
3 1 0 2
Cost: 1

Restart 15:
Iteration 1:
0 3 2 0
Cost: 3

Iteration 2:
1 3 2 0
Cost: 1

Restart 16:
Iteration 1:
1 2 1 2
Cost: 5

Iteration 2:
1 3 1 2
Cost: 2

Iteration 3:
1 3 0 2
Cost: 0

Restart 17:
Iteration 1:
3 0 3 3
Cost: 3

Iteration 2:
2 0 3 3
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Restart 18:
Iteration 1:
1 2 2 1
Cost: 4

Iteration 2:
0 2 2 1
Cost: 3

Iteration 3:
0 2 3 1
Cost: 1

Restart 19:
Iteration 1:
3 2 3 1
Cost: 3

Iteration 2:
0 2 3 1
Cost: 1

Restart 20:
Iteration 1:
1 1 0 0
Cost: 3

Iteration 2:
1 3 0 0
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 21:
Iteration 1:
3 0 1 0
Cost: 5

Iteration 2:
3 0 2 0
Cost: 2

Iteration 3:
3 0 2 1
Cost: 1

Restart 22:
Iteration 1:
0 1 3 1
Cost: 2

Iteration 2:
0 0 3 1
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Restart 23:
Iteration 1:
0 2 2 0
Cost: 4

Iteration 2:
1 2 2 0
Cost: 3

Iteration 3:
1 3 2 0
Cost: 1

Restart 24:
Iteration 1:
3 2 0 3
Cost: 2

Iteration 2:
1 2 0 3
Cost: 1

Restart 25:
Iteration 1:
3 2 3 0
Cost: 5

Iteration 2:
3 1 3 0
Cost: 2

Iteration 3:
2 1 3 0
Cost: 1

Restart 26:
Iteration 1:
0 1 0 1
Cost: 5

Iteration 2:
0 2 0 1
Cost: 2

Iteration 3:
0 2 3 1
Cost: 1

Restart 27:
Iteration 1:
1 3 1 0
Cost: 2

Iteration 2:
1 3 0 0
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 28:
Iteration 1:
1 2 2 3
Cost: 3

Iteration 2:
1 2 0 3
Cost: 1

Restart 29:
Iteration 1:
3 1 2 1
Cost: 3

Iteration 2:
3 0 2 1
Cost: 1

Restart 30:
Iteration 1:
0 2 0 2
Cost: 2

Iteration 2:
0 3 0 2
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 31:
Iteration 1:
3 1 2 2
Cost: 2

Iteration 2:
3 1 0 2
Cost: 1

Restart 32:
Iteration 1:
0 0 1 0
Cost: 5

Iteration 2:
0 3 1 0
Cost: 2

Iteration 3:
0 3 1 2
Cost: 1

Restart 33:
Iteration 1:
1 2 0 0
Cost: 3

Iteration 2:
1 3 0 0
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 34:
Iteration 1:
2 0 1 1
Cost: 2

Iteration 2:
2 0 3 1
Cost: 0

Restart 35:
Iteration 1:
0 3 3 3
Cost: 4

Iteration 2:
0 3 1 3
Cost: 2

Iteration 3:
0 3 1 2
Cost: 1

Restart 36:
Iteration 1:
1 2 3 2
Cost: 5

Iteration 2:
1 2 0 2
Cost: 2

Iteration 3:
1 3 0 2
Cost: 0

Restart 37:
Iteration 1:
1 1 2 1
Cost: 5

Iteration 2:
1 1 2 0
Cost: 2

Iteration 3:
1 3 2 0
Cost: 1

Restart 38:
Iteration 1:
3 2 1 0
Cost: 6

Iteration 2:
0 2 1 0
Cost: 4

Iteration 3:
0 3 1 0
Cost: 2

Iteration 4:
0 3 1 2
Cost: 1

Restart 39:
Iteration 1:
3 2 1 1
Cost: 4

Iteration 2:
0 2 1 1
Cost: 2

Iteration 3:
0 2 3 1
Cost: 1

Restart 40:
Iteration 1:
1 1 0 2
Cost: 2

Iteration 2:
1 3 0 2
Cost: 0

Restart 41:
Iteration 1:
1 1 1 1
Cost: 6

Iteration 2:
0 1 1 1
Cost: 4

Iteration 3:
0 2 1 1
Cost: 2

Iteration 4:
0 2 3 1
Cost: 1

Restart 42:
Iteration 1:
2 1 2 2
Cost: 5

Iteration 2:
3 1 2 2
Cost: 2

Iteration 3:
3 1 0 2
Cost: 1

Restart 43:
Iteration 1:
0 2 1 0
Cost: 4

Iteration 2:
0 3 1 0
Cost: 2

Iteration 3:
0 3 1 2
Cost: 1

Restart 44:
Iteration 1:
3 2 1 1
Cost: 4

Iteration 2:
0 2 1 1
Cost: 2

Iteration 3:
0 2 3 1
Cost: 1

Restart 45:
Iteration 1:
3 0 3 0
Cost: 3

Iteration 2:
2 0 3 0
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Restart 46:
Iteration 1:
3 0 2 0
Cost: 2

Iteration 2:
3 0 2 1
Cost: 1

Restart 47:
Iteration 1:
3 0 0 2
Cost: 2

Iteration 2:
3 1 0 2
Cost: 1

Restart 48:
Iteration 1:
0 0 0 2
Cost: 4

Iteration 2:
0 3 0 2
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 49:
Iteration 1:
0 1 2 0
Cost: 4

Iteration 2:
1 1 2 0
Cost: 2

Iteration 3:
1 3 2 0
Cost: 1

Restart 50:
Iteration 1:
0 0 1 1
Cost: 3

Iteration 2:
0 0 3 1
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Restart 51:
Iteration 1:
1 2 2 2
Cost: 4

Iteration 2:
1 3 2 2
Cost: 2

Iteration 3:
1 3 0 2
Cost: 0

Restart 52:
Iteration 1:
0 2 1 3
Cost: 2

Restart 53:
Iteration 1:
3 2 0 0
Cost: 4

Iteration 2:
3 2 0 1
Cost: 2

Restart 54:
Iteration 1:
1 1 0 3
Cost: 3

Iteration 2:
1 2 0 3
Cost: 1

Restart 55:
Iteration 1:
1 0 1 1
Cost: 5

Iteration 2:
2 0 1 1
Cost: 2

Iteration 3:
2 0 3 1
Cost: 0

Restart 56:
Iteration 1:
3 1 2 2
Cost: 2

Iteration 2:
3 1 0 2
Cost: 1

Restart 57:
Iteration 1:
3 1 2 3
Cost: 4

Iteration 2:
3 0 2 3
Cost: 2

Iteration 3:
3 0 2 1
Cost: 1

Restart 58:
Iteration 1:
1 1 2 1
Cost: 5

Iteration 2:
1 1 2 0
Cost: 2

Iteration 3:
1 3 2 0
Cost: 1

Restart 59:
Iteration 1:
2 2 3 2
Cost: 5

Iteration 2:
2 2 3 1
Cost: 2

Iteration 3:
2 0 3 1
Cost: 0

Restart 60:
Iteration 1:
0 3 1 2
Cost: 1

Restart 61:
Iteration 1:
2 2 2 3
Cost: 4

Iteration 2:
2 0 2 3
Cost: 2

Iteration 3:
2 0 1 3
Cost: 1

Restart 62:
Iteration 1:
3 0 0 3
Cost: 2

Restart 63:
Iteration 1:
0 1 2 0
Cost: 4

Iteration 2:
1 1 2 0
Cost: 2

Iteration 3:
1 3 2 0
Cost: 1

Restart 64:
Iteration 1:
2 2 2 1
Cost: 4

Iteration 2:
2 0 2 1
Cost: 2

Iteration 3:
2 0 3 1
Cost: 0

Restart 65:
Iteration 1:
3 2 0 0
Cost: 4

Iteration 2:
3 2 0 1
Cost: 2

Restart 66:
Iteration 1:
1 0 2 3
Cost: 2

Restart 67:
Iteration 1:
3 0 1 0
Cost: 5

Iteration 2:
3 0 2 0
Cost: 2

Iteration 3:
3 0 2 1
Cost: 1

Restart 68:
Iteration 1:
1 3 0 1
Cost: 3

Iteration 2:
1 3 0 2
Cost: 0

Restart 69:
Iteration 1:
3 1 2 1
Cost: 3

Iteration 2:
3 0 2 1
Cost: 1

Restart 70:
Iteration 1:
2 3 2 0
Cost: 3

Iteration 2:
1 3 2 0
Cost: 1

Restart 71:
Iteration 1:
2 1 2 0
Cost: 3

Iteration 2:
2 1 3 0
Cost: 1

Restart 72:
Iteration 1:
2 0 1 2
Cost: 4

Iteration 2:
2 0 1 3
Cost: 1

Restart 73:
Iteration 1:
1 2 3 1
Cost: 4

Iteration 2:
0 2 3 1
Cost: 1

Restart 74:
Iteration 1:
2 3 3 1
Cost: 3

Iteration 2:
2 0 3 1
Cost: 0

Restart 75:
Iteration 1:
2 2 3 1
Cost: 2

Iteration 2:
2 0 3 1
Cost: 0

Restart 76:
Iteration 1:
0 1 0 3
Cost: 5

Iteration 2:
0 2 0 3
Cost: 2

Iteration 3:
1 2 0 3
Cost: 1

Restart 77:
Iteration 1:
3 1 0 2
Cost: 1

Restart 78:
Iteration 1:
0 1 0 1
Cost: 5

Iteration 2:
0 2 0 1
Cost: 2

Iteration 3:
0 2 3 1
Cost: 1

Restart 79:
Iteration 1:
0 0 3 1
Cost: 1

Iteration 2:
2 0 3 1
Cost: 0

Restart 80:
Iteration 1:
0 0 2 1
Cost: 3

Iteration 2:
3 0 2 1
Cost: 1

Restart 81:
Iteration 1:
0 2 1 3
Cost: 2

Restart 82:
Iteration 1:
2 1 1 3
Cost: 3

Iteration 2:
2 0 1 3
Cost: 1

Restart 83:
Iteration 1:
0 2 0 1
Cost: 2

Iteration 2:
0 2 3 1
Cost: 1

Restart 84:
Iteration 1:
2 1 3 3
Cost: 3

Iteration 2:
2 0 3 3
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Restart 85:
Iteration 1:
1 0 2 0
Cost: 2

Iteration 2:
1 3 2 0
Cost: 1

Restart 86:
Iteration 1:
0 0 1 3
Cost: 3

Iteration 2:
2 0 1 3
Cost: 1

Restart 87:
Iteration 1:
2 0 0 1
Cost: 3

Iteration 2:
2 0 3 1
Cost: 0

Restart 88:
Iteration 1:
1 0 2 0
Cost: 2

Iteration 2:
1 3 2 0
Cost: 1

Restart 89:
Iteration 1:
2 1 3 1
Cost: 2

Iteration 2:
2 0 3 1
Cost: 0

Restart 90:
Iteration 1:
0 1 0 0
Cost: 5

Iteration 2:
0 1 3 0
Cost: 2

Iteration 3:
2 1 3 0
Cost: 1

Restart 91:
Iteration 1:
2 3 3 1
Cost: 3

Iteration 2:
2 0 3 1
Cost: 0

Restart 92:
Iteration 1:
3 2 0 2
Cost: 2

Iteration 2:
3 1 0 2
Cost: 1

Restart 93:
Iteration 1:
0 3 0 0
Cost: 3

Iteration 2:
1 3 0 0
Cost: 1

Iteration 3:
1 3 0 2
Cost: 0

Restart 94:
Iteration 1:
1 3 0 0
Cost: 1

Iteration 2:
1 3 0 2
Cost: 0

Restart 95:
Iteration 1:
3 1 0 1
Cost: 3

Iteration 2:
3 1 0 2
Cost: 1

Restart 96:
Iteration 1:
0 0 2 2
Cost: 4

Iteration 2:
3 0 2 2
Cost: 2

Iteration 3:
3 0 2 1
Cost: 1

Restart 97:
Iteration 1:
2 3 2 3
Cost: 5

Iteration 2:
2 0 2 3
Cost: 2

Iteration 3:
2 0 1 3
Cost: 1

Restart 98:
Iteration 1:
0 0 3 1
Cost: 1

Iteration 2:
2 0 3 1
Cost: 0

Restart 99:
Iteration 1:
3 2 3 1
Cost: 3

Iteration 2:
0 2 3 1
Cost: 1

Restart 100:
Iteration 1:
2 2 3 0
Cost: 3

Iteration 2:
2 0 3 0
Cost: 1

Iteration 3:
2 0 3 1
Cost: 0

Solution 1:
2 0 3 1

Solution 2:
1 3 0 2
