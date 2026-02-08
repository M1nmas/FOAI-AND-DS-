# ------ Semantic Network (Triples) -------
class SemanticNetwork:
    def __init__(self):
        self.triples = []
    def add(self, subject, predicate, obj):
        self.triples.append((subject, predicate, obj))
    def query(self, subject=None, predicate=None, obj=None):
        results = []
        for (s, p, o) in self.triples:
            if (subject is None or subject == s) and \
               (predicate is None or predicate == p) and \
               (obj is None or obj == o):
                results.append((s, p, o))
        return results
sn = SemanticNetwork()
sn.add("Bird", "is_a", "Animal")
sn.add("Parrot", "is_a", "Bird")
sn.add("Parrot", "has_color", "Green")

print("----- Semantic Network Example -----\n")

print("All facts about Parrot:")
print(sn.query(subject="Parrot"))

print("\nAll 'is a' relationships:")
print(sn.query(predicate="is_a"))
class Frame:
    def __init__(self, name, **slots):
        self.name = name
        self.slots = slots
    def get(self, slot):
        return self.slots.get(slot, "Unknown")
    def set(self, slot, value):
        self.slots[slot] = value
    def __repr__(self):
        return f"Frame({self.name}, {self.slots})"
parrot = Frame("Parrot", color="Green", can_fly=True, legs=2)
print(parrot)
print("Parrot color:", parrot.get("color"))
print("Parrot wings:", parrot.get("wings"))
parrot.set("wings", 2)
print("Updated Frame:", parrot)