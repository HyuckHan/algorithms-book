"""Same union-by-rank + path-compression DSU as DisjointSet.java/
disjoint_set.c -- newly written in Python, no canonical source exists."""


# snippet:disjoint-set:start
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        x, y = self.find(a), self.find(b)
        if x == y:
            return False
        if self.rank[x] < self.rank[y]:
            x, y = y, x
        self.parent[y] = x
        if self.rank[x] == self.rank[y]:
            self.rank[x] += 1
        return True
# snippet:disjoint-set:end


if __name__ == "__main__":
    d = DisjointSet(4)
    name = "ABCD"
    for u, v in [(0,1),(2,3),(1,2),(0,3)]:
        accepted = d.union(u, v)
        print(f"{name[u]}{name[v]}: {'accept' if accepted else 'reject'}")
    components = {}
    for v in range(4):
        components.setdefault(d.find(v), []).append(name[v])
    rendered = "".join("{" + ",".join(members) + "}" for members in components.values())
    print("components:", rendered)
