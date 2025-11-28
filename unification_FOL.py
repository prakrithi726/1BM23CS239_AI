# Implement unification in first order logic

def is_variable(x):
    return isinstance(x, str) and x[0].islower() and x.isalpha()

def is_compound(x):
    return isinstance(x, tuple) and len(x) > 0

def get_functor(x):
    return x[0] if is_compound(x) else None

def get_args(x):
    return list(x[1:]) if is_compound(x) else []

def occur_check(var, x, theta):
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    elif is_compound(x):
        return any(occur_check(var, arg, theta) for arg in get_args(x))
    else:
        return False

def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if theta == "failure":
        return "failure"
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif is_compound(x) and is_compound(y):
        if get_functor(x) != get_functor(y):
            return "failure"
        if len(get_args(x)) != len(get_args(y)):
            return "failure"
        return unify(get_args(x), get_args(y), theta)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return "failure"
        if not x:
            return theta
        first = unify(x[0], y[0], theta)
        return unify(x[1:], y[1:], first)
    else:
        return "failure"

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    elif occur_check(var, x, theta):
        return "failure"
    else:
        theta[var] = x
        return theta


# Test cases
expr1 = ("P", "x", ("h", "y"))
expr2 = ("P", "a", ("h", "b"))
print(unify(expr1, expr2))

expr3 = ("P", "x", ("h", "y"))
expr4 = ("P", "a", ("f", "z"))
print(unify(expr3, expr4))

expr5 = ("Knows", "John", "x")
expr6 = ("Knows", "x", "Elisabeth")
print(unify(expr5, expr6))

print()
print("Name: Prakrithi")
print("USN: 1BM23CS239")

output:
{'x': 'a', 'y': 'b'}
failure
failure

Name: Prakrithi
USN: 1BM23CS239
