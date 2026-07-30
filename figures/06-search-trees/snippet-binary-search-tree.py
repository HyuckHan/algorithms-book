class _Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = self.parent = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def _find(self, key):
        x = self.root
        while x is not None and x.key != key:
            x = x.left if key < x.key else x.right
        return x

    def contains(self, key):
        return self._find(key) is not None

    def insert(self, key):
        y, x = None, self.root
        while x is not None:
            y = x
            if key == x.key:
                return False
            x = x.left if key < x.key else x.right
        z = _Node(key)
        z.parent = y
        if y is None:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._size += 1
        return True

    @staticmethod
    def _minimum(x):
        if x is None:
            return None
        while x.left is not None:
            x = x.left
        return x

    @staticmethod
    def _maximum(x):
        if x is None:
            return None
        while x.right is not None:
            x = x.right
        return x

    def minimum(self):
        x = self._minimum(self.root)
        return None if x is None else x.key

    def maximum(self):
        x = self._maximum(self.root)
        return None if x is None else x.key

    @staticmethod
    def _successor(x):
        if x.right is not None:
            return BinarySearchTree._minimum(x.right)
        y = x.parent
        while y is not None and x is y.right:
            x, y = y, y.parent
        return y

    @staticmethod
    def _predecessor(x):
        if x.left is not None:
            return BinarySearchTree._maximum(x.left)
        y = x.parent
        while y is not None and x is y.left:
            x, y = y, y.parent
        return y

    def successor(self, key):
        x = self._find(key)
        if x is None:
            return None
        y = self._successor(x)
        return None if y is None else y.key

    def predecessor(self, key):
        x = self._find(key)
        if x is None:
            return None
        y = self._predecessor(x)
        return None if y is None else y.key

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def delete(self, key):
        z = self._find(key)
        if z is None:
            return False
        if z.left is None:
            self._transplant(z, z.right)
        elif z.right is None:
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            if y.parent is not z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
        self._size -= 1
        return True

    def inorder(self):
        out = []

        def walk(x):
            if x is not None:
                walk(x.left)
                out.append(x.key)
                walk(x.right)

        walk(self.root)
        return out
