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
