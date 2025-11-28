# Forward reasoning in First Order Logic

from itertools import product

def is_variable(x):
    return isinstance(x, str) and x[0].islower()


def substitute(theta, x):
    if isinstance(x, tuple):
        return (x[0], [substitute(theta, arg) for arg in x[1]])
    elif isinstance(x, list):
        return [substitute(theta, xi) for xi in x]
    else:
        return theta.get(x, x)


def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if theta == "fail":
        return "fail"
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x[1]) != len(y[1]):
            return "fail"
        return unify(x[1], y[1], theta)
    elif isinstance(x, list) and isinstance(y, list):
        if not x and not y:
            return theta
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return "fail"


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    elif occurs_check(var, x, theta):
        return "fail"
    else:
        new_theta = theta.copy()
        new_theta[var] = x
        return new_theta


def occurs_check(var, x, theta):
    if var == x:
        return True
    elif isinstance(x, list):
        return any(occurs_check(var, xi, theta) for xi in x)
    elif isinstance(x, tuple):
        return occurs_check(var, x[1], theta)
    elif x in theta:
        return occurs_check(var, theta[x], theta)
    return False


# Predicate constructor
def pred(name, *args):
    return (name, list(args))


# ---------------------------
# Forward chaining algorithm
# ---------------------------

def fol_fc_ask(KB, query, trace=True):
    inferred = set(map(str, KB["facts"]))
    new_inferred = True
    iteration = 0

    while new_inferred:
        iteration += 1
        new_inferred = False

        if trace:
            print(f"\n--- Iteration {iteration} ---")

        for rule in KB["rules"]:
            premises, conclusion = rule

            possible_bindings = [list(inferred) for _ in premises]

            for facts_combo in product(*possible_bindings):
                theta = {}
                ok = True

                for premise, fact in zip(premises, facts_combo):
                    fact = eval(fact)
                    theta = unify(premise, fact, theta)
                    if theta == "fail":
                        ok = False
                        break

                if not ok:
                    continue

                inferred_fact = substitute(theta, conclusion)
                inferred_str = str(inferred_fact)

                if inferred_str not in inferred:
                    inferred.add(inferred_str)
                    new_inferred = True

                    if trace:
                        print(f"Derived new fact: {inferred_fact} from {premises}")

                if unify(inferred_fact, query) != "fail":
                    if trace:
                        print(f"\nDerived goal successfully: {query}")
                    return True

    return False


# ---------------------------
# MAIN PROGRAM
# ---------------------------

if __name__ == "__main__":
    KB = {
        "facts": [
            pred("American", "West"),
            pred("Missile", "M1"),
            pred("Owns", "Nono", "M1"),
            pred("Enemy", "Nono", "America")
        ],
        "rules": [
            (
                [pred("American", "x"), pred("Weapon", "y"),
                 pred("Sells", "x", "y", "z"), pred("Hostile", "z")],
                pred("Criminal", "x")
            ),
            (
                [pred("Missile", "x")],
                pred("Weapon", "x")
            ),
            (
                [pred("Missile", "x"), pred("Owns", "Nono", "x")],
                pred("Sells", "West", "x", "Nono")
            ),
            (
                [pred("Enemy", "x", "America")],
                pred("Hostile", "x")
            )
        ]
    }

    query = pred("Criminal", "West")

    print("Inference process:")
    result = fol_fc_ask(KB, query)

    if result:
        print("\nConclusion: West is a Criminal.")
    else:
        print("\nCould not prove the query.")

    print()
    print("Name: Prakrithi")
    print("USN: 1BM23CS239")
output:
nference process:

--- Iteration 1 ---
Derived new fact: ('Weapon', ['M1']) from [('Missile', ['x'])]
Derived new fact: ('Sells', ['West', 'M1', 'Nono']) from [('Missile', ['x']), ('Owns', ['Nono', 'x'])]
Derived new fact: ('Hostile', ['Nono']) from [('Enemy', ['x', 'America'])]

--- Iteration 2 ---
Derived new fact: ('Criminal', ['West']) from [('American', ['x']), ('Weapon', ['y']), ('Sells', ['x', 'y', 'z']), ('Hostile', ['z'])]

Derived goal successfully: ('Criminal', ['West'])

Conclusion: West is a Criminal.

Name: Prakrithi
USN: 1BM23CS239
