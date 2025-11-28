# Implement Alpha-Beta Pruning.
import math

class Node:
    def __init__(self, value=None, children=None, is_max=True):
        self.value = value
        self.children = children or []
        self.is_max = is_max

def alpha_beta(node, alpha=-math.inf, beta=math.inf):
    if not node.children:
        return node.value

    if node.is_max:
        value = -math.inf
        for child in node.children:
            value = max(value, alpha_beta(child, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        node.value = value
        return value
    else:
        value = math.inf
        for child in node.children:
            value = min(value, alpha_beta(child, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        node.value = value
        return value

def print_tree(node, level=0):
    indent = " " * level
    if not node.children:
        print(f"{indent}Leaf Node (value={node.value})")
    else:
        role = "MAX" if node.is_max else "MIN"
        print(f"{indent}{role} Node (value={node.value})")
        for child in node.children:
            print_tree(child, level + 1)

def build_tree_from_leaves(leaf_values, branching_factor, is_max=True):
    current_level_nodes = [Node(value=v, is_max=not is_max) for v in leaf_values]
    level = 1

    while len(current_level_nodes) > 1:
        next_level_nodes = []
        for i in range(0, len(current_level_nodes), branching_factor):
            children = current_level_nodes[i:i + branching_factor]
            node = Node(children=children, is_max=(level % 2 == 0))
            next_level_nodes.append(node)
        current_level_nodes = next_level_nodes
        level += 1

    root = current_level_nodes[0]
    root.is_max = True
    return root

if __name__ == "__main__":
    branching_factor = int(input("Enter number of branches per node: "))
    num_leaves = int(input("Enter total number of leaf nodes: "))

    depth = math.log(num_leaves, branching_factor) + 1
    if abs(round(depth) - depth) > 1e-9:
        print("\n Error: The number of leaves must form a full tree (b^(d-1)).")
        print(" Example: With 3 branches, leaf count = 3, 9, 27, ...")
        exit()

    depth = int(round(depth))
    print(f"\nTree depth will be {depth} levels (including root).")

    leaf_values = []
    print("\nEnter the values for each leaf node (can be number, inf, -inf):")
    for i in range(num_leaves):
        val = input(f"Leaf {i+1}: ").strip()
        if val.lower() == "inf":
            val = math.inf
        elif val.lower() == "-inf":
            val = -math.inf
        else:
            val = float(val)
        leaf_values.append(val)

    root = build_tree_from_leaves(leaf_values, branching_factor, is_max=True)
    best_value = alpha_beta(root)

    print("\n=== Alpha-Beta Pruning Result ===")
    print(f"Best value for root: {best_value}\n")

    print("=== Game Tree ===")
    print_tree(root)

    print()
    print("Name: Prakrithi")
    print("USN: 1BM23CS239")

output:
Enter number of branches per node: 3
Enter total number of leaf nodes: 9

Tree depth will be 3 levels (including root).

Enter the values for each leaf node (can be number, inf, -inf):
Leaf 1: 1
Leaf 2: 3
Leaf 3: 5
Leaf 4: 2
Leaf 5: 10
Leaf 6: 16
Leaf 7: 18
Leaf 8: 19
Leaf 9: 20

=== Alpha-Beta Pruning Result ===
Best value for root: 18.0

=== Game Tree ===
MAX Node (value=18.0)
 MIN Node (value=1.0)
  Leaf Node (value=1.0)
  Leaf Node (value=3.0)
  Leaf Node (value=5.0)
 MIN Node (value=2.0)
  Leaf Node (value=2.0)
  Leaf Node (value=10.0)
  Leaf Node (value=16.0)
 MIN Node (value=18.0)
  Leaf Node (value=18.0)
  Leaf Node (value=19.0)
  Leaf Node (value=20.0)

Name: Prakrithi
USN: 1BM23CS239
