"""BTree: distinct int key, CLRS minimum degree t, top-down split-before-
descend insert, borrow/merge delete. lecture-notes/code/lecture06/java/
BTree.java와 같은 정책·예제 입력(t=2)을 쓴다."""


# snippet:btree:start
class _Node:
    def __init__(self, leaf):
        self.keys = []
        self.children = []
        self.leaf = leaf


def _lower_bound(a, k):
    i = 0
    while i < len(a) and a[i] < k:
        i += 1
    return i


class BTree:
    def __init__(self, minimum_degree):
        if minimum_degree < 2:
            raise ValueError("t >= 2")
        self.t = minimum_degree
        self.root = _Node(True)
        self._size = 0

    def __len__(self):
        return self._size

    def contains(self, k):
        return self._contains(self.root, k)

    def _contains(self, x, k):
        i = _lower_bound(x.keys, k)
        if i < len(x.keys) and x.keys[i] == k:
            return True
        return (not x.leaf) and self._contains(x.children[i], k)

    def insert(self, k):
        if self.contains(k):
            return False
        t = self.t
        if len(self.root.keys) == 2 * t - 1:
            s = _Node(False)
            s.children.append(self.root)
            self._split_child(s, 0)
            self.root = s
        self._insert_nonfull(self.root, k)
        self._size += 1
        return True

    def _insert_nonfull(self, x, k):
        i = _lower_bound(x.keys, k)
        if x.leaf:
            x.keys.insert(i, k)
            return
        t = self.t
        if len(x.children[i].keys) == 2 * t - 1:
            self._split_child(x, i)
            if k > x.keys[i]:
                i += 1
        self._insert_nonfull(x.children[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = _Node(y.leaf)
        median = y.keys[t - 1]
        z.keys = y.keys[t:2 * t - 1]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:2 * t]
            y.children = y.children[:t]
        x.keys.insert(i, median)
        x.children.insert(i + 1, z)

    def delete(self, k):
        if not self.contains(k):
            return False
        self._delete(self.root, k)
        if not self.root.keys and not self.root.leaf:
            self.root = self.root.children[0]
        self._size -= 1
        return True

    def _delete(self, x, k):
        t = self.t
        i = _lower_bound(x.keys, k)
        if i < len(x.keys) and x.keys[i] == k:
            if x.leaf:
                x.keys.pop(i)
            elif len(x.children[i].keys) >= t:
                pred = self._max(x.children[i])
                x.keys[i] = pred
                self._delete(x.children[i], pred)
            elif len(x.children[i + 1].keys) >= t:
                succ = self._min(x.children[i + 1])
                x.keys[i] = succ
                self._delete(x.children[i + 1], succ)
            else:
                self._merge(x, i)
                self._delete(x.children[i], k)
            return
        child = i
        if len(x.children[child].keys) == t - 1:
            if child > 0 and len(x.children[child - 1].keys) >= t:
                self._borrow_prev(x, child)
            elif child < len(x.children) - 1 and len(x.children[child + 1].keys) >= t:
                self._borrow_next(x, child)
            else:
                if child < len(x.children) - 1:
                    self._merge(x, child)
                else:
                    self._merge(x, child - 1)
                    child -= 1
        self._delete(x.children[child], k)

    def _min(self, x):
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]

    def _max(self, x):
        while not x.leaf:
            x = x.children[-1]
        return x.keys[-1]

    def _borrow_prev(self, x, i):
        c, s = x.children[i], x.children[i - 1]
        c.keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = s.keys.pop()
        if not c.leaf:
            c.children.insert(0, s.children.pop())

    def _borrow_next(self, x, i):
        c, s = x.children[i], x.children[i + 1]
        c.keys.append(x.keys[i])
        x.keys[i] = s.keys.pop(0)
        if not c.leaf:
            c.children.append(s.children.pop(0))

    def _merge(self, x, i):
        c, s = x.children[i], x.children.pop(i + 1)
        c.keys.append(x.keys.pop(i))
        c.keys.extend(s.keys)
        if not c.leaf:
            c.children.extend(s.children)

    def inorder(self):
        out = []

        def walk(x):
            for i, key in enumerate(x.keys):
                if not x.leaf:
                    walk(x.children[i])
                out.append(key)
            if not x.leaf:
                walk(x.children[len(x.keys)])

        walk(self.root)
        return out
# snippet:btree:end

if __name__ == "__main__":
    t = BTree(2)
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        t.insert(k)
    print("inorder:", ",".join(str(k) for k in t.inorder()))
    print("size:", len(t))
    print("root:", ",".join(str(k) for k in t.root.keys))
    print("children:", ";".join(",".join(str(k) for k in c.keys) for c in t.root.children))
    for k in [6, 7, 5, 10, 12, 17, 20, 30]:
        t.delete(k)
    print("delete size:", len(t))
