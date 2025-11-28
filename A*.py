# A* algorithm using Manhattan distance
import heapq
GOAL_STATE = (1, 2, 3, 8, 0, 4, 7, 6, 5)
NEIGHBORS = {
0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
}
def manhattan_distance(state):
distance = 0
for i, tile in enumerate(state):
if tile == 0:
continue
goal_pos = GOAL_STATE.index(tile)
x1, y1 = divmod(i, 3)
x2, y2 = divmod(goal_pos, 3)
distance += abs(x1 - x2) + abs(y1 - y2)
return distance
def get_neighbors(state):
zero_index = state.index(0)
neighbors = []
for swap_index in NEIGHBORS[zero_index]:
new_state = list(state)
new_state[zero_index], new_state[swap_index] = new_state[swap_index],
new_state[zero_index]
neighbors.append(tuple(new_state))
return neighbors
def reconstruct_path(came_from, current):
path = [current]
while current in came_from:
current = came_from[current]
path.append(current)
path.reverse()
return path
def a_star_manhattan(start_state):
open_set = []
heapq.heappush(open_set, (manhattan_distance(start_state), 0, start_state))
came_from = {}
g_score = {start_state: 0}
closed_set = set()
18
while open_set:
f, g, current = heapq.heappop(open_set)
if current == GOAL_STATE:
return reconstruct_path(came_from, current)
closed_set.add(current)
for neighbor in get_neighbors(current):
if neighbor in closed_set:
continue
tentative_g = g + 1
if tentative_g < g_score.get(neighbor, float('inf')):
came_from[neighbor] = current
g_score[neighbor] = tentative_g
f_score = tentative_g + manhattan_distance(neighbor)
heapq.heappush(open_set, (f_score, tentative_g, neighbor))
return None
if __name__ == "__main__":
start = (2, 8, 3, 1, 6, 4, 7, 0, 5)
path = a_star_manhattan(start)
if path:
print("Solution using Manhattan Distance heuristic:")
for state in path:
print(state[:3], state[3:6], state[6:], sep="\n", end="\n\n")
print(f"Total cost: {len(path) - 1}")
else:
print("No solution found.")
print("Name: Prakrithi Jain")
print("USN: 1BM23CS239")

output:
(2, 8, 3)
(1, 6, 4)
(7, 0, 5)

(2, 8, 3)
(1, 0, 4)
(7, 6, 5)

(2, 0, 3)
(1, 8, 4)
(7, 6, 5)

(0, 2, 3)
(1, 8, 4)
(7, 6, 5)

(1, 2, 3)
(0, 8, 4)
(7, 6, 5)

(1, 2, 3)
(8, 0, 4)
(7, 6, 5)

Total cost: 5
Name: Prakrithi Jain
USN: 1BM23CS239
