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
