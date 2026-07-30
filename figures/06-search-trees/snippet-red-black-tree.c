/* RedBlackTree: distinct int key with one shared black NIL sentinel,
 * z/p/g/u 용어(current/parent/grandparent/uncle). O(log n) 연산.
 * lecture-notes/code/lecture06/java/RedBlackTree.java와 같은 정책·예제를 C로 옮긴 것이다. */
typedef enum { RED, BLACK } Color;

typedef struct Node {
    int key;
    Color color;
    struct Node *left, *right, *parent;
} Node;

typedef struct {
    Node nil_storage;
    Node *nil;
    Node *root;
    int size;
} Rbt;

static void rbt_init(Rbt *t) {
    t->nil = &t->nil_storage;
    t->nil->color = BLACK;
    t->nil->left = t->nil->right = t->nil->parent = t->nil;
    t->root = t->nil;
    t->size = 0;
}

static Node *rbt_find(Rbt *t, int key) {
    Node *x = t->root;
    while (x != t->nil && x->key != key) x = key < x->key ? x->left : x->right;
    return x;
}

static void rotate_left(Rbt *t, Node *x) {
    Node *y = x->right;
    x->right = y->left;
    if (y->left != t->nil) y->left->parent = x;
    y->parent = x->parent;
    if (x->parent == t->nil) t->root = y;
    else if (x == x->parent->left) x->parent->left = y;
    else x->parent->right = y;
    y->left = x; x->parent = y;
}

static void rotate_right(Rbt *t, Node *y) {
    Node *x = y->left;
    y->left = x->right;
    if (x->right != t->nil) x->right->parent = y;
    x->parent = y->parent;
    if (y->parent == t->nil) t->root = x;
    else if (y == y->parent->left) y->parent->left = x;
    else y->parent->right = x;
    x->right = y; y->parent = x;
}

static void insert_fixup(Rbt *t, Node *z) {
    while (z->parent->color == RED) {
        if (z->parent == z->parent->parent->left) {
            Node *u = z->parent->parent->right;
            if (u->color == RED) {
                z->parent->color = BLACK; u->color = BLACK;
                z->parent->parent->color = RED; z = z->parent->parent;
            } else {
                if (z == z->parent->right) { z = z->parent; rotate_left(t, z); }
                z->parent->color = BLACK; z->parent->parent->color = RED;
                rotate_right(t, z->parent->parent);
            }
        } else {
            Node *u = z->parent->parent->left;
            if (u->color == RED) {
                z->parent->color = BLACK; u->color = BLACK;
                z->parent->parent->color = RED; z = z->parent->parent;
            } else {
                if (z == z->parent->left) { z = z->parent; rotate_right(t, z); }
                z->parent->color = BLACK; z->parent->parent->color = RED;
                rotate_left(t, z->parent->parent);
            }
        }
    }
    t->root->color = BLACK;
    t->root->parent = t->nil;
}

static bool rbt_insert(Rbt *t, int key) {
    Node *y = t->nil, *x = t->root;
    while (x != t->nil) {
        y = x;
        if (key == x->key) return false;
        x = key < x->key ? x->left : x->right;
    }
    Node *z = malloc(sizeof *z);
    z->key = key; z->color = RED; z->left = z->right = t->nil; z->parent = y;
    if (y == t->nil) t->root = z;
    else if (key < y->key) y->left = z;
    else y->right = z;
    t->size++;
    insert_fixup(t, z);
    return true;
}

static Node *rbt_minimum(Rbt *t, Node *x) {
    while (x->left != t->nil) x = x->left;
    return x;
}

static void rbt_transplant(Rbt *t, Node *u, Node *v) {
    if (u->parent == t->nil) t->root = v;
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    v->parent = u->parent;
}

static void delete_fixup(Rbt *t, Node *x) {
    while (x != t->root && x->color == BLACK) {
        if (x == x->parent->left) {
            Node *w = x->parent->right;
            if (w->color == RED) {
                w->color = BLACK; x->parent->color = RED;
                rotate_left(t, x->parent); w = x->parent->right;
            }
            if (w->left->color == BLACK && w->right->color == BLACK) {
                w->color = RED; x = x->parent;
            } else {
                if (w->right->color == BLACK) {
                    w->left->color = BLACK; w->color = RED;
                    rotate_right(t, w); w = x->parent->right;
                }
                w->color = x->parent->color; x->parent->color = BLACK;
                w->right->color = BLACK; rotate_left(t, x->parent); x = t->root;
            }
        } else {
            Node *w = x->parent->left;
            if (w->color == RED) {
                w->color = BLACK; x->parent->color = RED;
                rotate_right(t, x->parent); w = x->parent->left;
            }
            if (w->right->color == BLACK && w->left->color == BLACK) {
                w->color = RED; x = x->parent;
            } else {
                if (w->left->color == BLACK) {
                    w->right->color = BLACK; w->color = RED;
                    rotate_left(t, w); w = x->parent->left;
                }
                w->color = x->parent->color; x->parent->color = BLACK;
                w->left->color = BLACK; rotate_right(t, x->parent); x = t->root;
            }
        }
    }
    x->color = BLACK;
}

static bool rbt_delete(Rbt *t, int key) {
    Node *z = rbt_find(t, key);
    if (z == t->nil) return false;
    Node *y = z, *x;
    Color original = y->color;
    if (z->left == t->nil) { x = z->right; rbt_transplant(t, z, z->right); }
    else if (z->right == t->nil) { x = z->left; rbt_transplant(t, z, z->left); }
    else {
        y = rbt_minimum(t, z->right);
        original = y->color;
        x = y->right;
        if (y->parent == z) x->parent = y;
        else {
            rbt_transplant(t, y, y->right);
            y->right = z->right; y->right->parent = y;
        }
        rbt_transplant(t, z, y);
        y->left = z->left; y->left->parent = y; y->color = z->color;
    }
    t->size--;
    if (original == BLACK) delete_fixup(t, x);
    if (t->root != t->nil) t->root->parent = t->nil;
    else t->nil->parent = t->nil;
    return true;
}

static void rbt_inorder(Rbt *t, const Node *x, int *out, int *n) {
    if (x == t->nil) return;
    rbt_inorder(t, x->left, out, n);
    out[(*n)++] = x->key;
    rbt_inorder(t, x->right, out, n);
}
