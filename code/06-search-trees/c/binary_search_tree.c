#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

// snippet:binary-search-tree:start
/* BinarySearchTree: distinct int key, parent pointer, SEARCH/MINIMUM/MAXIMUM/
 * SUCCESSOR/PREDECESSOR/INSERT/DELETE(Transplant 기반) 전부 O(h).
 * 강의노트 원본과 같은 정책·예제를 C로 옮긴 것이다. */
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
// snippet:binary-search-tree:end

static void print_ints(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

static void print_opt(const char *label, bool present, int value) {
    if (present) printf("%s: %d\n", label, value);
    else printf("%s: none\n", label);
}

int main(void) {
    Bst t = {0};
    int seed[] = {15, 6, 3, 2, 4, 7, 13, 9, 14, 18, 17, 20};
    for (size_t i = 0; i < sizeof seed / sizeof seed[0]; i++) bst_insert(&t, seed[i]);

    int out[32], n = 0, v;
    bst_inorder(t.root, out, &n);
    print_ints("inorder", out, n);

    bst_insert(&t, 12);
    n = 0; bst_inorder(t.root, out, &n);
    print_ints("insert12 inorder", out, n);

    bst_minimum(&t, &v); printf("minimum: %d\n", v);
    bst_maximum(&t, &v); printf("maximum: %d\n", v);
    /* Each call site's mutating lookup is a separate statement from the
     * print, so argument-evaluation order (unspecified by C when a
     * function's own out-parameter and its plain-value argument appear in
     * the same call) can't read `v` before the lookup writes it. */
    bool found = bst_successor(&t, 15, &v); print_opt("successor15", found, v);
    found = bst_successor(&t, 6, &v); print_opt("successor6", found, v);
    found = bst_successor(&t, 4, &v); print_opt("successor4", found, v);
    found = bst_successor(&t, 20, &v); print_opt("successor20", found, v);
    found = bst_predecessor(&t, 15, &v); print_opt("predecessor15", found, v);

    bst_delete(&t, 6);
    n = 0; bst_inorder(t.root, out, &n);
    print_ints("delete6 inorder", out, n);

    bst_delete(&t, 15);
    n = 0; bst_inorder(t.root, out, &n);
    print_ints("delete15 inorder", out, n);
    return 0;
}
