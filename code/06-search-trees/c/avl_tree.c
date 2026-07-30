#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

// snippet:avl-tree:start
/* AVLTree: distinct int key. empty height=-1, leaf height=0, BF=left-right.
 * lecture-notes/code/lecture06/java/AVLTree.java와 같은 정책·예제를 C로 옮긴 것이다. */
typedef struct Node {
    int key, height;
    struct Node *left, *right;
} Node;

static int node_height(const Node *x) { return x == NULL ? -1 : x->height; }

static void node_update(Node *x) {
    int l = node_height(x->left), r = node_height(x->right);
    x->height = 1 + (l > r ? l : r);
}

static int node_bf(const Node *x) { return node_height(x->left) - node_height(x->right); }

static Node *rotate_right(Node *y) {
    Node *x = y->left, *b = x->right;
    x->right = y; y->left = b;
    node_update(y); node_update(x);
    return x;
}

static Node *rotate_left(Node *x) {
    Node *y = x->right, *b = y->left;
    y->left = x; x->right = b;
    node_update(x); node_update(y);
    return y;
}

static Node *rebalance(Node *x) {
    node_update(x);
    if (node_bf(x) > 1) {
        if (node_bf(x->left) < 0) x->left = rotate_left(x->left);
        return rotate_right(x);
    }
    if (node_bf(x) < -1) {
        if (node_bf(x->right) > 0) x->right = rotate_right(x->right);
        return rotate_left(x);
    }
    return x;
}

static bool avl_contains(const Node *x, int k) {
    while (x != NULL) {
        if (k == x->key) return true;
        x = k < x->key ? x->left : x->right;
    }
    return false;
}

static Node *avl_insert_node(Node *x, int k) {
    if (x == NULL) {
        Node *n = malloc(sizeof *n);
        n->key = k; n->height = 0; n->left = n->right = NULL;
        return n;
    }
    if (k < x->key) x->left = avl_insert_node(x->left, k);
    else x->right = avl_insert_node(x->right, k);
    return rebalance(x);
}

static void avl_inorder(const Node *x, int *out, int *n) {
    if (x == NULL) return;
    avl_inorder(x->left, out, n);
    out[(*n)++] = x->key;
    avl_inorder(x->right, out, n);
}
// snippet:avl-tree:end

typedef struct { Node *root; } Avl;

static bool avl_insert(Avl *t, int k) {
    if (avl_contains(t->root, k)) return false;
    t->root = avl_insert_node(t->root, k);
    return true;
}

static void print_ints(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

static void run_case(const char *name, const int *seq, int len) {
    Avl t = {0};
    for (int i = 0; i < len; i++) avl_insert(&t, seq[i]);
    int out[16], n = 0;
    avl_inorder(t.root, out, &n);
    char label[32];
    snprintf(label, sizeof label, "%s inorder", name);
    print_ints(label, out, n);
    printf("%s height: %d\n", name, node_height(t.root));
}

int main(void) {
    int ll[] = {30, 20, 10};
    int rr[] = {10, 20, 30};
    int lr[] = {30, 10, 20};
    int rl[] = {10, 30, 20};
    run_case("LL", ll, 3);
    run_case("RR", rr, 3);
    run_case("LR", lr, 3);
    run_case("RL", rl, 3);

    Avl big = {0};
    for (int i = 0; i < 15; i++) avl_insert(&big, i);
    printf("sequential15 height: %d\n", node_height(big.root));
    int out[16], n = 0;
    avl_inorder(big.root, out, &n);
    print_ints("sequential15 inorder", out, n);
    return 0;
}
