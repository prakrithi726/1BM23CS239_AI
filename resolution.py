from itertools import combinations, product
from copy import deepcopy

def negate_literal(lit: str) -> str:
    """Negate a literal string. '~P(a)' <-> 'P(a)'"""
    lit = lit.strip()
    return lit[1:] if lit.startswith("~") else "~" + lit

def is_variable(x: str) -> bool:
    """Consider a string starting with lowercase letter as variable."""
    return isinstance(x, str) and len(x) > 0 and x[0].islower()

def get_predicate(literal: str) -> str:
    """Return predicate name from literal like 'P(a,b)' or '~P(a)' -> 'P'"""
    lit = literal[1:] if literal.startswith("~") else literal
    return lit[:lit.find("(")].strip()

def get_args_from_literal(literal: str):
    """Return argument list from literal string as list of strings."""
    lit = literal[1:] if literal.startswith("~") else literal
    inside = lit[lit.find("(") + 1: -1].strip()
    if inside == "":
        return []
    return [arg.strip() for arg in inside.split(",")]

def literal_to_tuple(literal: str):
    """Convert literal string to tuple form (negated:boolean, predicate, [args])"""
    neg = literal.startswith("~")
    pred = get_predicate(literal)
    args = get_args_from_literal(literal)
    return (neg, pred, args)

def tuple_to_literal(tup):
    """Convert tuple form (neg, pred, args) back to literal string."""
    neg, pred, args = tup
    args_s = ", ".join(args)
    lit = f"{pred}({args_s})"
    return ("~" + lit) if neg else lit

def substitute_in_arg(arg, subs):
    """Apply substitution dict to a single argument recursively."""
    # if arg is variable and in subs, replace; otherwise return arg
    if is_variable(arg) and arg in subs:
        return subs[arg]
    return arg

def substitute_literal(literal: str, subs: dict) -> str:
    """Apply substitution to literal string and return new literal string."""
    neg, pred, args = literal_to_tuple(literal)
    new_args = [substitute_in_arg(a, subs) for a in args]
    return tuple_to_literal((neg, pred, new_args))

# ---------------------------
# Unification (simple, for terms that are variables/constants)
# Returns substitution dict or 'failure'
# ---------------------------

def occur_check(var, x, theta):
    """Prevent var -> ...var... circular substitutions."""
    if var == x:
        return True
    if is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    return False

def unify_var(var, x, theta):
    """Unify variable var with term x under theta (dict)."""
    if var in theta:
        return unify(theta[var], x, theta)
    if is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    if occur_check(var, x, theta):
        return "failure"
    new_theta = theta.copy()
    new_theta[var] = x
    return new_theta

def unify(x, y, theta=None):
    """
    Unify two terms x and y.
    x and y are strings (variables or constants) or lists of such strings (argument lists).
    Returns substitution dict or 'failure'.
    """
    if theta is None:
        theta = {}

    # If theta already failure
    if theta == "failure":
        return "failure"

    # If identical
    if x == y:
        return theta

    # variable cases
    if isinstance(x, str) and is_variable(x):
        return unify_var(x, y, theta)
    if isinstance(y, str) and is_variable(y):
        return unify_var(y, x, theta)

    # lists of arguments
    if isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return "failure"
        if not x and not y:
            return theta
        # unify head then tail
        theta1 = unify(x[0], y[0], theta)
        if theta1 == "failure":
            return "failure"
        return unify(x[1:], y[1:], theta1)

    # constants (strings) that are different cannot unify
    if isinstance(x, str) and isinstance(y, str) and x != y:
        return "failure"

    return "failure"

# ---------------------------
# Resolution + unification
# ---------------------------

def standardize_apart(clause, index):
    """
    Standardize variables in a clause by renaming them with a suffix based on index.
    clause is set of literal strings.
    """
    subs = {}
    new_clause = set()
    for lit in clause:
        neg, pred, args = literal_to_tuple(lit)
        new_args = []
        for a in args:
            if is_variable(a):
                if a not in subs:
                    subs[a] = f"{a}_{index}"
                new_args.append(subs[a])
            else:
                new_args.append(a)
        new_clause.add(tuple_to_literal((neg, pred, new_args)))
    return new_clause

def resolve(ci, cj, idx_i=0, idx_j=0):
    """
    Attempt to resolve clauses ci and cj (sets of literal strings).
    Returns set of resolvent clauses (each as frozenset of literal strings).
    Uses unification when predicates are complementary up to variable substitution.
    """
    resolvents = set()
    # Standardize apart to avoid variable name clashes
    ci_std = standardize_apart(ci, idx_i)
    cj_std = standardize_apart(cj, idx_j)

    for lit_i in ci_std:
        for lit_j in cj_std:
            neg_i = lit_i.startswith("~")
            neg_j = lit_j.startswith("~")
            pred_i = get_predicate(lit_i)
            pred_j = get_predicate(lit_j)

            # Only try to resolve if predicates same and signs opposite
            if pred_i == pred_j and neg_i != neg_j:
                args_i = get_args_from_literal(lit_i)
                args_j = get_args_from_literal(lit_j)

                # when one is negated, unify the positive with the positive args
                # create term tuples for unification (lists)
                # remove negation for unify input
                # unify returns substitution mapping variables -> terms
                unifier = unify(args_i, args_j, {})

                if unifier != "failure":
                    # Build new clause: (ci \ {lit_i}) U (cj \ {lit_j}) with substitution applied
                    new_ci = {substitute_literal(l, unifier) for l in (ci_std - {lit_i})}
                    new_cj = {substitute_literal(l, unifier) for l in (cj_std - {lit_j})}
                    new_clause = frozenset(new_ci | new_cj)

                    resolvents.add(new_clause)

    return resolvents

def resolution(kb_clauses, query, max_iterations=1000, trace=True):
    """
    kb_clauses: iterable of clauses (each clause is an iterable of literal strings)
    query: literal string to prove (e.g., "Likes(John,Peanuts)")
    Returns True if query is proved (i.e., empty clause derived), otherwise False.
    """
    # Convert to frozenset of frozenset literals
    kb = set(frozenset(c) for c in kb_clauses)

    # Add negated query as a clause
    neg_query = frozenset([negate_literal(query)])
    kb.add(neg_query)

    new = set()
    clauses_list = list(kb)
    iteration = 0

    while True:
        iteration += 1
        if trace:
            print(f"\nIteration {iteration}: KB size = {len(kb)}")

        pairs = list(combinations(list(kb), 2))
        generated_this_round = set()

        # use unique indices to standardize apart
        for idx, (ci, cj) in enumerate(pairs):
            resolvents = resolve(set(ci), set(cj), idx_i=iteration + idx, idx_j=iteration + idx + 10000)
            if trace and resolvents:
                print(f"Resolving\n  {set(ci)}\n  {set(cj)}\n  -> {resolvents}")
            for res in resolvents:
                if len(res) == 0:
                    if trace:
                        print("\nDerived empty clause -> contradiction (query proved).")
                    return True
                if res not in kb and res not in new and res not in generated_this_round:
                    generated_this_round.add(res)

        if not generated_this_round:
            return False

        # Add newly generated clauses to kb and continue
        for c in generated_this_round:
            new.add(c)
        kb = kb.union(generated_this_round)

        # safety to prevent infinite loop
        if iteration >= max_iterations:
            if trace:
                print("Reached max iterations without deriving empty clause.")
            return False



if __name__ == "__main__":
    # Build KB: represent each clause as a set (or list) of literal strings
    kb = [
        {"~Food(x)", "Likes(John, x)"},
        {"Food(Peanuts)"},
        {"Food(Apple)"},
        {"Food(Vegetables)"},
        {"~Eats(x, y)", "Killed(x)", "Food(y)"},
        {"Eats(Anil, Peanuts)"},
        {"Alive(Anil)"},
        {"~Eats(Anil, y)", "Eats(Harry, y)"},
        {"~Alive(x)", "~Killed(x)"},
        {"Killed(x)", "Alive(x)"}
    ]

    query = "Likes(John, Peanuts)"

    print("Knowledge Base (clauses):")
    for c in kb:
        print(c)

    proved = resolution(kb, query, trace=True)

    print("\nResult:")
    if proved:
        print(f"Query proved: {query}")
    else:
        print(f"Could not prove the query: {query}")

    print()
    print("Name: Prakrithi")
    print("USN: 1BM23CS239")

output:
Knowledge Base (clauses):
{'~Food(x)', 'Likes(John, x)'}
{'Food(Peanuts)'}
{'Food(Apple)'}
{'Food(Vegetables)'}
{'Killed(x)', 'Food(y)', '~Eats(x, y)'}
{'Eats(Anil, Peanuts)'}
{'Alive(Anil)'}
{'~Eats(Anil, y)', 'Eats(Harry, y)'}
{'~Alive(x)', '~Killed(x)'}
{'Killed(x)', 'Alive(x)'}

Iteration 1: KB size = 11
Resolving
  {'Alive(Anil)'}
  {'~Alive(x)', '~Killed(x)'}
  -> {frozenset({'~Killed(Anil)'})}
Resolving
  {'Eats(Anil, Peanuts)'}
  {'Killed(x)', 'Food(y)', '~Eats(x, y)'}
  -> {frozenset({'Food(Peanuts)', 'Killed(Anil)'})}
Resolving
  {'Eats(Anil, Peanuts)'}
  {'~Eats(Anil, y)', 'Eats(Harry, y)'}
  -> {frozenset({'Eats(Harry, Peanuts)'})}
Resolving
  {'~Alive(x)', '~Killed(x)'}
  {'Killed(x)', 'Alive(x)'}
  -> {frozenset({'Killed(x_10020)', '~Killed(x_10020)'}), frozenset({'Alive(x_10020)', '~Alive(x_10020)'})}
Resolving
  {'~Alive(x)', '~Killed(x)'}
  {'Killed(x)', 'Food(y)', '~Eats(x, y)'}
  -> {frozenset({'Food(y_10023)', '~Eats(x_10023, y_10023)', '~Alive(x_10023)'})}
Resolving
  {'Food(Apple)'}
  {'~Food(x)', 'Likes(John, x)'}
  -> {frozenset({'Likes(John, Apple)'})}
Resolving
  {'~Likes(John, Peanuts)'}
  {'~Food(x)', 'Likes(John, x)'}
  -> {frozenset({'~Food(Peanuts)'})}
Resolving
  {'Killed(x)', 'Food(y)', '~Eats(x, y)'}
  {'~Food(x)', 'Likes(John, x)'}
  -> {frozenset({'Likes(John, x_10046)', 'Killed(x_46)', '~Eats(x_46, x_10046)'})}
Resolving
  {'Killed(x)', 'Food(y)', '~Eats(x, y)'}
  {'~Eats(Anil, y)', 'Eats(Harry, y)'}
  -> {frozenset({'Killed(Harry)', 'Food(y_10049)', '~Eats(Anil, y_10049)'})}
Resolving
  {'~Food(x)', 'Likes(John, x)'}
  {'Food(Peanuts)'}
  -> {frozenset({'Likes(John, Peanuts)'})}
Resolving
  {'~Food(x)', 'Likes(John, x)'}
  {'Food(Vegetables)'}
  -> {frozenset({'Likes(John, Vegetables)'})}

Iteration 2: KB size = 23
Resolving
  {'Likes(John, Peanuts)'}
  {'~Likes(John, Peanuts)'}
  -> {frozenset()}

Derived empty clause -> contradiction (query proved).

Result:
Query proved: Likes(John, Peanuts)

Name: Prakrithi
USN: 1BM23CS239
