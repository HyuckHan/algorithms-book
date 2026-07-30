/* BinarySearchTree: distinct int key, parent pointer, SEARCH/MINIMUM/MAXIMUM/
 * SUCCESSOR/PREDECESSOR/INSERT/DELETE(Transplant 기반) 전부 O(h).
 * lecture-notes/code/lecture06/java/BinarySearchTree.java와 같은 정책·예제를 C로 옮긴 것이다. */
typedef struct Node {
    int key;
    struct Node *left, *right, *parent;
} Node;

typedef struct {
    Node *root;
    int size;
} Bst;

static Node *bst_find(Bst *t, int key) {
    Node *x = t->root;
    while (x != NULL && x->key != key) x = key < x->key ? x->left : x->right;
    return x;
}

static bool bst_insert(Bst *t, int key) {
    Node *y = NULL, *x = t->root;
    while (x != NULL) {
        y = x;
        if (key == x->key) return false;
        x = key < x->key ? x->left : x->right;
    }
    Node *z = malloc(sizeof *z);
    z->key = key; z->left = z->right = NULL; z->parent = y;
    if (y == NULL) t->root = z;
    else if (key < y->key) y->left = z;
    else y->right = z;
    t->size++;
    return true;
}

static Node *bst_minimum_node(Node *x) {
    if (x == NULL) return NULL;
    while (x->left != NULL) x = x->left;
    return x;
}

static Node *bst_maximum_node(Node *x) {
    if (x == NULL) return NULL;
    while (x->right != NULL) x = x->right;
    return x;
}

static bool bst_minimum(Bst *t, int *out) {
    Node *x = bst_minimum_node(t->root);
    if (x == NULL) return false;
    *out = x->key; return true;
}

static bool bst_maximum(Bst *t, int *out) {
    Node *x = bst_maximum_node(t->root);
    if (x == NULL) return false;
    *out = x->key; return true;
}

static Node *node_successor(Node *x) {
    if (x->right != NULL) return bst_minimum_node(x->right);
    Node *y = x->parent;
    while (y != NULL && x == y->right) { x = y; y = y->parent; }
    return y;
}

static Node *node_predecessor(Node *x) {
    if (x->left != NULL) return bst_maximum_node(x->left);
    Node *y = x->parent;
    while (y != NULL && x == y->left) { x = y; y = y->parent; }
    return y;
}

static bool bst_successor(Bst *t, int key, int *out) {
    Node *x = bst_find(t, key);
    if (x == NULL) return false;
    Node *y = node_successor(x);
    if (y == NULL) return false;
    *out = y->key; return true;
}

static bool bst_predecessor(Bst *t, int key, int *out) {
    Node *x = bst_find(t, key);
    if (x == NULL) return false;
    Node *y = node_predecessor(x);
    if (y == NULL) return false;
    *out = y->key; return true;
}

static void bst_transplant(Bst *t, Node *u, Node *v) {
    if (u->parent == NULL) t->root = v;
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    if (v != NULL) v->parent = u->parent;
}

static bool bst_delete(Bst *t, int key) {
    Node *z = bst_find(t, key);
    if (z == NULL) return false;
    if (z->left == NULL) bst_transplant(t, z, z->right);
    else if (z->right == NULL) bst_transplant(t, z, z->left);
    else {
        Node *y = bst_minimum_node(z->right);
        if (y->parent != z) {
            bst_transplant(t, y, y->right);
            y->right = z->right; y->right->parent = y;
        }
        bst_transplant(t, z, y);
        y->left = z->left; y->left->parent = y;
    }
    t->size--;
    return true;
}

static void bst_inorder(const Node *x, int *out, int *n) {
    if (x == NULL) return;
    bst_inorder(x->left, out, n);
    out[(*n)++] = x->key;
    bst_inorder(x->right, out, n);
}
