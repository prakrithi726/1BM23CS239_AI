# Simulated Annealing for N-Queens (All Steps)
# Fully corrected and Colab-ready

import numpy as np
from scipy.optimize import dual_annealing

# ------------------------------
# Cost Function
# ------------------------------
def calculate_cost(board):
    cost = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                cost += 1
    return cost


def cost_function(board):
    board = np.round(board).astype(int)
    return calculate_cost(board)


# ------------------------------
# Log Intermediate Steps
# ------------------------------
def log_intermediate_results(x, f, context):
    iteration_data.append((np.round(x).astype(int), f))


# ------------------------------
# Simulated Annealing Solver
# ------------------------------
def solve_8_queens(n=8, max_restarts=100):
    bounds = [(0, n - 1)] * n
    unique_solutions = set()
    all_iterations = []

    for _ in range(max_restarts):
        global iteration_data
        iteration_data = []

        result = dual_annealing(cost_function, bounds, callback=log_intermediate_results)

        solution = np.round(result.x).astype(int)
        cost = result.fun

        all_iterations.append(iteration_data)

        if cost == 0:
            unique_solutions.add(tuple(solution))

    return list(unique_solutions), all_iterations


def print_solution(board):
    print(" ".join(map(str, board)))


# ------------------------------
# MAIN EXECUTION
# ------------------------------
solutions, all_iterations = solve_8_queens()

print("All Iterations for Each Restart:\n")
for restart_idx, iterations in enumerate(all_iterations):
    print(f"Restart {restart_idx + 1}:")
    for step_idx, (board_state, cost) in enumerate(iterations):
        print(f"Iteration {step_idx + 1}:")
        print("State (Queen positions):", board_state)
        print("Cost:", cost)
        print()

print("Unique Solutions Found:\n")
for idx, solution in enumerate(solutions):
    print(f"Solution {idx + 1}:")
    print_solution(solution)
    print()

print("Name: Prakrithi")
print("USN: 1BM23CS239")

output:
Restart 1:
Iteration 1:
State (Queen positions): [6 3 5 2 7 4 1 0]
Cost: 7

Iteration 2:
State (Queen positions): [6 3 5 2 0 4 1 7]
Cost: 6

Iteration 3:
State (Queen positions): [1 3 5 2 0 4 6 7]
Cost: 4

Iteration 4:
State (Queen positions): [1 3 5 7 0 4 6 2]
Cost: 2

Iteration 5:
State (Queen positions): [1 3 5 7 2 0 6 4]
Cost: 1

Iteration 6:
State (Queen positions): [1 3 5 7 2 4 6 0]
Cost: 0


Restart 2:
Iteration 1:
State (Queen positions): [2 5 7 1 3 0 6 4]
Cost: 5

Iteration 2:
State (Queen positions): [2 5 7 1 3 6 0 4]
Cost: 3

Iteration 3:
State (Queen positions): [4 6 1 5 2 0 3 7]
Cost: 2

Iteration 4:
State (Queen positions): [4 6 1 5 2 7 3 0]
Cost: 0


Restart 3:
Iteration 1:
State (Queen positions): [0 4 7 5 2 6 1 3]
Cost: 1

Iteration 2:
State (Queen positions): [0 4 7 5 2 6 1 3]
Cost: 0


Unique Solutions Found:

Solution 1:
1 3 5 7 2 4 6 0

Solution 2:
4 6 1 5 2 7 3 0

Solution 3:
0 4 7 5 2 6 1 3


Name: Prakrithi
USN: 1BM23CS239
