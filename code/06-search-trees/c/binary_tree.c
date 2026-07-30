#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// snippet:binary-tree:start
/* BinaryTree: 4가지 traversal과 size/height. empty height=-1, leaf height=0.
 * lecture-notes/code/lecture06/java/BinaryTree.java와 같은 정책·예제를 C로 옮긴 것이다. */
typedef struct Node {
    const char *data;
    struct Node *left, *right;
} Node;

static Node *node_new(const char *data, Node *left, Node *right) {
    Node *n = malloc(sizeof *n);
    n->data = data;
    n->left = left;
    n->right = right;
    return n;
}

static void preorder(const Node *x, const char **out, int *n) {
    if (x == NULL) return;
    out[(*n)++] = x->data;
    preorder(x->left, out, n);
    preorder(x->right, out, n);
}

static void inorder(const Node *x, const char **out, int *n) {
    if (x == NULL) return;
    inorder(x->left, out, n);
    out[(*n)++] = x->data;
    inorder(x->right, out, n);
}

static void postorder(const Node *x, const char **out, int *n) {
    if (x == NULL) return;
    postorder(x->left, out, n);
    postorder(x->right, out, n);
    out[(*n)++] = x->data;
}

static void level_order(const Node *root, const char **out, int *n) {
    if (root == NULL) return;
    const Node *queue[64];
    int head = 0, tail = 0;
    queue[tail++] = root;
    while (head < tail) {
        const Node *x = queue[head++];
        out[(*n)++] = x->data;
        if (x->left != NULL) queue[tail++] = x->left;
        if (x->right != NULL) queue[tail++] = x->right;
    }
}

static int tree_size(const Node *x) {
    return x == NULL ? 0 : 1 + tree_size(x->left) + tree_size(x->right);
}

static int tree_height(const Node *x) {
    if (x == NULL) return -1;
    int l = tree_height(x->left), r = tree_height(x->right);
    return 1 + (l > r ? l : r);
}
// snippet:binary-tree:end

static void print_list(const char *label, const char **items, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%s%s", items[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    Node *b = node_new("B", node_new("D", NULL, NULL), node_new("E", NULL, NULL));
    Node *c = node_new("C", node_new("F", NULL, NULL), node_new("G", NULL, NULL));
    Node *t = node_new("A", b, c);

    const char *out[16];
    int n;

    n = 0; preorder(t, out, &n); print_list("preorder", out, n);
    n = 0; inorder(t, out, &n); print_list("inorder", out, n);
    n = 0; postorder(t, out, &n); print_list("postorder", out, n);
    n = 0; level_order(t, out, &n); print_list("levelorder", out, n);
    printf("size: %d\n", tree_size(t));
    printf("height: %d\n", tree_height(t));
    return 0;
}
