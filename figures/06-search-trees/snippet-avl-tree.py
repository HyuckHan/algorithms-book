class _Node:
    def __init__(self, key):
        self.key = key
        self.height = 0
        self.left = self.right = None


def _h(x):
    return -1 if x is None else x.height


def _update(x):
    x.height = 1 + max(_h(x.left), _h(x.right))


def _bf(x):
    return _h(x.left) - _h(x.right)


def _rotate_right(y):
    x = y.left
    b = x.right
    x.right = y
    y.left = b
    _update(y)
    _update(x)
    return x


def _rotate_left(x):
    y = x.right
    b = y.left
    y.left = x
    x.right = b
    _update(x)
    _update(y)
    return y


def _rebalance(x):
    _update(x)
    if _bf(x) > 1:
        if _bf(x.left) < 0:
            x.left = _rotate_left(x.left)
        return _rotate_right(x)
    if _bf(x) < -1:
        if _bf(x.right) > 0:
            x.right = _rotate_right(x.right)
        return _rotate_left(x)
    return x


class AVLTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def contains(self, key):
        x = self.root
        while x is not None:
            if key == x.key:
                return True
            x = x.left if key < x.key else x.right
        return False

    def insert(self, key):
        if self.contains(key):
            return False
        self.root = self._insert(self.root, key)
        self._size += 1
        return True

    def _insert(self, x, key):
        if x is None:
            return _Node(key)
        if key < x.key:
            x.left = self._insert(x.left, key)
        else:
            x.right = self._insert(x.right, key)
        return _rebalance(x)

    def height(self):
        return _h(self.root)

    def inorder(self):
        out = []

        def walk(x):
            if x is not None:
                walk(x.left)
                out.append(x.key)
                walk(x.right)

        walk(self.root)
        return out
