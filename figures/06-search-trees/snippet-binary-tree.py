class Node:
    def __init__(self, data, left=None, right=None):
        if data is None:
            raise ValueError("data must not be None")
        self.data = data
        self.left = left
        self.right = right


def preorder(x):
    if x is None:
        return []
    return [x.data] + preorder(x.left) + preorder(x.right)


def inorder(x):
    if x is None:
        return []
    return inorder(x.left) + [x.data] + inorder(x.right)


def postorder(x):
    if x is None:
        return []
    return postorder(x.left) + postorder(x.right) + [x.data]


def level_order(root):
    if root is None:
        return []
    out = []
    q = deque([root])
    while q:
        x = q.popleft()
        out.append(x.data)
        if x.left is not None:
            q.append(x.left)
        if x.right is not None:
            q.append(x.right)
    return out


def size(x):
    return 0 if x is None else 1 + size(x.left) + size(x.right)


def height(x):
    return -1 if x is None else 1 + max(height(x.left), height(x.right))
