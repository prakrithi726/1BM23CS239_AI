# Knowledge Base using Propositional Logic
# Supports AND, OR, NOT, IMPLIES, IFF
from itertools import product

def AND(p, q): return p and q
def OR(p, q): return p or q
def NOT(p): return not p
def IMPLIES(p, q): return (not p) or q
def IFF(p, q): return p == q

class Formula:
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def evaluate(self, assignment):
        if isinstance(self.op, str) and len(self.args) == 0:
            return assignment[self.op]

        if self.op == 'AND':
            return AND(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'OR':
            return OR(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'NOT':
            return NOT(self.args[0].evaluate(assignment))
        elif self.op == 'IMPLIES':
            return IMPLIES(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        elif self.op == 'IFF':
            return IFF(self.args[0].evaluate(assignment), self.args[1].evaluate(assignment))
        else:
            raise ValueError(f"Unknown operator: {self.op}")

    def __str__(self):
        if isinstance(self.op, str) and len(self.args) == 0:
            return self.op
        elif self.op == 'NOT':
            return f"¬{self.args[0]}"
        elif self.op == 'AND':
            return f"({self.args[0]} ∧ {self.args[1]})"
        elif self.op == 'OR':
            return f"({self.args[0]} ∨ {self.args[1]})"
        elif self.op == 'IMPLIES':
            return f"({self.args[0]} → {self.args[1]})"
        elif self.op == 'IFF':
            return f"({self.args[0]} ↔ {self.args[1]})"
        return f"UnknownOp({self.op})"


def extract_symbols(formula):
    symbols = set()
    if isinstance(formula.op, str) and len(formula.args) == 0:
        symbols.add(formula.op)
    else:
        for arg in formula.args:
            symbols |= extract_symbols(arg)
    return symbols


def extract_subformulas(formula):
    subs = {formula}
    for arg in formula.args:
        subs |= extract_subformulas(arg)
    return subs

def entails(KB, alpha):
    symbols = sorted(list(extract_symbols(KB) | extract_symbols(alpha)))

    print("Knowledge Base (KB):", KB)
    print("Alpha (Query):", alpha)
    print()

    sub_KB = extract_subformulas(KB)
    sub_alpha = extract_subformulas(alpha)

    all_subformulas = list(sub_KB | sub_alpha)
    all_subformulas = [f for f in all_subformulas if not (isinstance(f.op, str) and len(f.args) == 0)]
    all_subformulas.sort(key=lambda f: str(f))

    headers = symbols + [str(f) for f in all_subformulas] + ["KB", "Alpha"]
    print(" | ".join(f"{h:^12}" for h in headers))
    print("-" * (15 * len(headers)))

    failing_case_found = False

    for values in product([False, True], repeat=len(symbols)):
        assignment = dict(zip(symbols, values))

        sub_vals = [f.evaluate(assignment) for f in all_subformulas]
        kb_val = KB.evaluate(assignment)
        alpha_val = alpha.evaluate(assignment)

        row_vals = (
            ['T' if assignment[s] else 'F' for s in symbols] +
            ['T' if v else 'F' for v in sub_vals] +
            ['T' if kb_val else 'F', 'T' if alpha_val else 'F']
        )

        print(" | ".join(f"{v:^12}" for v in row_vals))

        if kb_val and not alpha_val:
            failing_case_found = True

    print()
    if failing_case_found:
        print("Result: KB does NOT entail Alpha.")
        return False

    print("Result: KB entails Alpha.")
    return True
#KB base and query

A = Formula('A')
B = Formula('B')
C = Formula('C')

KB = Formula('IFF',
             Formula('IMPLIES',
                     Formula('AND', A, Formula('NOT', B)),
                     Formula('OR', C, A)),
             Formula('OR', B, Formula('NOT', C))
)

alpha = Formula('IMPLIES', A, C)

result = entails(KB, alpha)
print("\nDoes KB entail alpha?", result)

print("\nName: Prakrithi")
print("USN: 1BM23CS239")

output:
Knowledge Base (KB): (((A ∧ ¬B) → (C ∨ A)) ↔ (B ∨ ¬C))
Alpha (Query): (A → C)

     A       |      B       |      C       | (((A ∧ ¬B) → (C ∨ A)) ↔ (B ∨ ¬C)) | ((A ∧ ¬B) → (C ∨ A)) |   (A → C)    |   (A ∧ ¬B)   |   (B ∨ ¬C)   |   (C ∨ A)    |      ¬B      |      ¬C      |      KB      |    Alpha    
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     F       |      F       |      F       |      T       |      T       |      T       |      F       |      T       |      F       |      T       |      T       |      T       |      T      
     F       |      F       |      T       |      F       |      T       |      T       |      F       |      F       |      T       |      T       |      F       |      F       |      T      
     F       |      T       |      F       |      T       |      T       |      T       |      F       |      T       |      F       |      F       |      T       |      T       |      T      
     F       |      T       |      T       |      T       |      T       |      T       |      F       |      T       |      T       |      F       |      F       |      T       |      T      
     T       |      F       |      F       |      T       |      T       |      F       |      T       |      T       |      T       |      T       |      T       |      T       |      F      
     T       |      F       |      T       |      F       |      T       |      T       |      T       |      F       |      T       |      T       |      F       |      F       |      T      
     T       |      T       |      F       |      T       |      T       |      F       |      F       |      T       |      T       |      F       |      T       |      T       |      F      
     T       |      T       |      T       |      T       |      T       |      T       |      F       |      T       |      T       |      F       |      F       |      T       |      T      

Result: KB does NOT entail Alpha.

Does KB entail alpha? False

Name: Prakrithi
USN: 1BM23CS239
