# AND Introduction Inference
P = True
Q = True
if P and Q:
    R = True
else:
    R = False
print("Inference Result (P AND Q):", R)
# Propositional Logic Inference - Real World Example
raining = True
raining_implies_umbrella = True
if raining and raining_implies_umbrella:
    take_umbrella = True
else:
    take_umbrella = False
if take_umbrella:
    print("Inference Result: Take an umbrella")
else:
    print("Inference Result: No umbrella needed")
# Forward chaining inference
def forward_chaining(facts, rules):
    inferred = set(facts)
    changed = True
    while changed:
        changed = False
        for head, body in rules:
            if body.issubset(inferred) and head not in inferred:
                inferred.add(head)
                changed = True
    return inferred
if __name__ == "__main__":
    facts = {"rain", "cold"}
    rules = [
        ("wet", {"rain"}),
        ("slippery", {"wet"}),
        ("stay_home", {"cold", "rain"}),
    ]
    result = forward_chaining(facts, rules)
    print("Initial Facts:", facts)
    print("Inferred Facts:", result)