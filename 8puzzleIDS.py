from collections import deque

# ------------------------ Goal state ------------------------
GOAL = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)  # 0 = blank

# ------------------------ Helpers ---------------------------
def format_state(state):
    return f"{state[0]} {state[1]} {state[2]}\n{state[3]} {state[4]} {state[5]}\n{state[6]} {state[7]} {state[8]}"

def get_neighbors(state):
    """Return possible next states (new_state, move_char)."""
    i = state.index(0)
    r, c = divmod(i, 3)
    moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    for dr, dc, act in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            lst = list(state)
            lst[i], lst[j] = lst[j], lst[i]
            yield tuple(lst), act

# ------------------------ Depth-Limited DFS -----------------
def dls(state, limit, path, pathset):
    if state == GOAL:
        return path
    if limit == 0:
        return None
    for nbr, act in get_neighbors(state):
        if nbr in pathset:
            continue
        pathset.add(nbr)
        res = dls(nbr, limit - 1, path + [act], pathset)
        if res is not None:
            return res
        pathset.remove(nbr)
    return None

# ------------------------ IDS -------------------------------
def ids(start, max_depth=50):
    for depth in range(max_depth + 1):
        pathset = {start}
        result = dls(start, depth, [], pathset)
        if result is not None:
            return result, depth
    return None, None

# ------------------------ Run Example -----------------------
if __name__ == "__main__":
    start = (2, 8, 3,
             1, 6, 4,
             7, 0, 5)

    path, depth = ids(start, max_depth=10)

    if path is None:
        print("No solution found.")
    else:
        print("IDS Solution found!")
        print("Moves:", "".join(path))
        print("Number of moves:", len(path))
        print("Depth reached:", depth)

        # Show board step by step
        cur = start
        print("\nStart:\n" + format_state(cur))
        for m in path:
            for nbr, act in get_neighbors(cur):
                if act == m:
                    cur = nbr
                    break
            print(f"\nMove: {m}\n{format_state(cur)}")
IDS Solution found!
Moves: UULDR
Number of moves: 5
Depth reached: 5

Start:
2 8 3
1 6 4
7 0 5

Move: U
2 8 3
1 0 4
7 6 5

Move: U
2 0 3
1 8 4
7 6 5

Move: L
0 2 3
1 8 4
7 6 5

Move: D
1 2 3
0 8 4
7 6 5

Move: R
1 2 3
8 0 4
7 6 5
