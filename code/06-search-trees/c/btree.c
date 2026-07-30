#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

// snippet:btree:start
/* BTree: distinct int key, CLRS minimum degree t, top-down split-before-
 * descend insert, borrow/merge delete.
 * lecture-notes/code/lecture06/java/BTree.java와 같은 정책·예제(t=2)를 C로 옮긴 것이다. */
#define MAX_KEYS 15 /* 2*t-1 for t up to 8, plenty for this chapter's t in {2,3,5} */
#define MAX_CHILDREN (MAX_KEYS + 1)

typedef struct Node {
    int keys[MAX_KEYS];
    int nkeys;
    struct Node *children[MAX_CHILDREN];
    bool leaf;
} Node;

typedef struct {
    int t;
    Node *root;
    int size;
} BTree;

static Node *node_new(bool leaf) {
    Node *n = malloc(sizeof *n);
    n->nkeys = 0;
    n->leaf = leaf;
    return n;
}

static void btree_init(BTree *b, int minimum_degree) {
    b->t = minimum_degree;
    b->root = node_new(true);
    b->size = 0;
}

static int lower_bound(const int *a, int n, int k) {
    int i = 0;
    while (i < n && a[i] < k) i++;
    return i;
}

static bool node_contains(const Node *x, int k) {
    int i = lower_bound(x->keys, x->nkeys, k);
    if (i < x->nkeys && x->keys[i] == k) return true;
    return !x->leaf && node_contains(x->children[i], k);
}

static bool btree_contains(BTree *b, int k) { return node_contains(b->root, k); }

static void split_child(BTree *b, Node *x, int i) {
    int t = b->t;
    Node *y = x->children[i];
    Node *z = node_new(y->leaf);
    int median = y->keys[t - 1];

    z->nkeys = t - 1;
    for (int j = 0; j < t - 1; j++) z->keys[j] = y->keys[t + j];
    if (!y->leaf) {
        for (int j = 0; j < t; j++) z->children[j] = y->children[t + j];
    }
    y->nkeys = t - 1;

    for (int j = x->nkeys; j > i; j--) x->keys[j] = x->keys[j - 1];
    for (int j = x->nkeys + 1; j > i + 1; j--) x->children[j] = x->children[j - 1];
    x->keys[i] = median;
    x->children[i + 1] = z;
    x->nkeys++;
}

static void insert_nonfull(BTree *b, Node *x, int k) {
    int i = lower_bound(x->keys, x->nkeys, k);
    if (x->leaf) {
        for (int j = x->nkeys; j > i; j--) x->keys[j] = x->keys[j - 1];
        x->keys[i] = k;
        x->nkeys++;
        return;
    }
    if (x->children[i]->nkeys == 2 * b->t - 1) {
        split_child(b, x, i);
        if (k > x->keys[i]) i++;
    }
    insert_nonfull(b, x->children[i], k);
}

static bool btree_insert(BTree *b, int k) {
    if (btree_contains(b, k)) return false;
    if (b->root->nkeys == 2 * b->t - 1) {
        Node *s = node_new(false);
        s->children[0] = b->root;
        b->root = s;
        split_child(b, s, 0);
    }
    insert_nonfull(b, b->root, k);
    b->size++;
    return true;
}

static int subtree_min(Node *x) {
    while (!x->leaf) x = x->children[0];
    return x->keys[0];
}

static int subtree_max(Node *x) {
    while (!x->leaf) x = x->children[x->nkeys];
    return x->keys[x->nkeys - 1];
}

static void merge_children(BTree *b, Node *x, int i) {
    Node *c = x->children[i], *s = x->children[i + 1];
    c->keys[c->nkeys] = x->keys[i];
    for (int j = 0; j < s->nkeys; j++) c->keys[c->nkeys + 1 + j] = s->keys[j];
    if (!c->leaf) {
        for (int j = 0; j <= s->nkeys; j++) c->children[c->nkeys + 1 + j] = s->children[j];
    }
    c->nkeys += 1 + s->nkeys;
    for (int j = i; j < x->nkeys - 1; j++) x->keys[j] = x->keys[j + 1];
    for (int j = i + 1; j < x->nkeys; j++) x->children[j] = x->children[j + 1];
    x->nkeys--;
    free(s);
    (void)b;
}

static void borrow_prev(Node *x, int i) {
    Node *c = x->children[i], *s = x->children[i - 1];
    for (int j = c->nkeys; j > 0; j--) c->keys[j] = c->keys[j - 1];
    c->keys[0] = x->keys[i - 1];
    x->keys[i - 1] = s->keys[s->nkeys - 1];
    if (!c->leaf) {
        for (int j = c->nkeys + 1; j > 0; j--) c->children[j] = c->children[j - 1];
        c->children[0] = s->children[s->nkeys];
    }
    c->nkeys++;
    s->nkeys--;
}

static void borrow_next(Node *x, int i) {
    Node *c = x->children[i], *s = x->children[i + 1];
    c->keys[c->nkeys] = x->keys[i];
    x->keys[i] = s->keys[0];
    if (!c->leaf) c->children[c->nkeys + 1] = s->children[0];
    c->nkeys++;
    for (int j = 0; j < s->nkeys - 1; j++) s->keys[j] = s->keys[j + 1];
    if (!s->leaf) {
        for (int j = 0; j < s->nkeys; j++) s->children[j] = s->children[j + 1];
    }
    s->nkeys--;
}

static void btree_delete_node(BTree *b, Node *x, int k) {
    int t = b->t;
    int i = lower_bound(x->keys, x->nkeys, k);
    if (i < x->nkeys && x->keys[i] == k) {
        if (x->leaf) {
            for (int j = i; j < x->nkeys - 1; j++) x->keys[j] = x->keys[j + 1];
            x->nkeys--;
        } else if (x->children[i]->nkeys >= t) {
            int pred = subtree_max(x->children[i]);
            x->keys[i] = pred;
            btree_delete_node(b, x->children[i], pred);
        } else if (x->children[i + 1]->nkeys >= t) {
            int succ = subtree_min(x->children[i + 1]);
            x->keys[i] = succ;
            btree_delete_node(b, x->children[i + 1], succ);
        } else {
            merge_children(b, x, i);
            btree_delete_node(b, x->children[i], k);
        }
        return;
    }
    int child = i;
    if (x->children[child]->nkeys == t - 1) {
        if (child > 0 && x->children[child - 1]->nkeys >= t) borrow_prev(x, child);
        else if (child < x->nkeys && x->children[child + 1]->nkeys >= t) borrow_next(x, child);
        else if (child < x->nkeys) merge_children(b, x, child);
        else { merge_children(b, x, child - 1); child--; }
    }
    btree_delete_node(b, x->children[child], k);
}

static bool btree_delete(BTree *b, int k) {
    if (!btree_contains(b, k)) return false;
    btree_delete_node(b, b->root, k);
    if (b->root->nkeys == 0 && !b->root->leaf) {
        Node *old = b->root;
        b->root = b->root->children[0];
        free(old);
    }
    b->size--;
    return true;
}

static void btree_inorder(const Node *x, int *out, int *n) {
    for (int i = 0; i < x->nkeys; i++) {
        if (!x->leaf) btree_inorder(x->children[i], out, n);
        out[(*n)++] = x->keys[i];
    }
    if (!x->leaf) btree_inorder(x->children[x->nkeys], out, n);
}
// snippet:btree:end

static void print_ints(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    BTree b;
    btree_init(&b, 2);
    int seed[] = {10, 20, 5, 6, 12, 30, 7, 17};
    for (size_t i = 0; i < sizeof seed / sizeof seed[0]; i++) btree_insert(&b, seed[i]);

    int out[16], n = 0;
    btree_inorder(b.root, out, &n);
    print_ints("inorder", out, n);
    print_ints("root", b.root->keys, b.root->nkeys);

    printf("children: ");
    for (int i = 0; i <= b.root->nkeys; i++) {
        for (int j = 0; j < b.root->children[i]->nkeys; j++) {
            printf("%d%s", b.root->children[i]->keys[j],
                   j + 1 < b.root->children[i]->nkeys ? "," : "");
        }
        if (i < b.root->nkeys) printf(";");
    }
    printf("\n");

    int del[] = {6, 7, 5, 10, 12, 17, 20, 30};
    for (size_t i = 0; i < sizeof del / sizeof del[0]; i++) btree_delete(&b, del[i]);
    printf("size: %d\n", b.size);
    return 0;
}
