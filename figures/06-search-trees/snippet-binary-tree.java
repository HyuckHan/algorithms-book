    private static final class Node<E> {
        E data;
        Node<E> left, right;
        Node(E data) { this.data = Objects.requireNonNull(data); }
    }
    private Node<E> root;

    public BinaryTree() {}
    public BinaryTree(E data) { root = new Node<>(data); }
    /** Deep-copies both subtrees, so the new tree owns all nodes. */
    public BinaryTree(E data, BinaryTree<E> left, BinaryTree<E> right) {
        root = new Node<>(data);
        root.left = copy(left == null ? null : left.root);
        root.right = copy(right == null ? null : right.root);
    }
    private BinaryTree(Node<E> source) { root = copy(source); }
    private static <E> Node<E> copy(Node<E> x) {
        if (x == null) return null;
        Node<E> y = new Node<>(x.data);
        y.left = copy(x.left); y.right = copy(x.right); return y;
    }

    public boolean isEmpty() { return root == null; }
    public Optional<E> rootData() {
        return root == null ? Optional.empty() : Optional.of(root.data);
    }
    public BinaryTree<E> leftSubtree() {
        return new BinaryTree<>(root == null ? null : root.left);
    }
    public BinaryTree<E> rightSubtree() {
        return new BinaryTree<>(root == null ? null : root.right);
    }
    public int size() { return size(root); }
    private static int size(Node<?> x) {
        return x == null ? 0 : 1 + size(x.left) + size(x.right);
    }
    public int height() { return height(root); }
    private static int height(Node<?> x) {
        return x == null ? -1 : 1 + Math.max(height(x.left), height(x.right));
    }

    public List<E> preorder() {
        List<E> out = new ArrayList<>(); preorder(root, out); return List.copyOf(out);
    }
    private static <E> void preorder(Node<E> x, List<E> out) {
        if (x == null) return;
        out.add(x.data); preorder(x.left, out); preorder(x.right, out);
    }
    public List<E> inorder() {
        List<E> out = new ArrayList<>(); inorder(root, out); return List.copyOf(out);
    }
    private static <E> void inorder(Node<E> x, List<E> out) {
        if (x == null) return;
        inorder(x.left, out); out.add(x.data); inorder(x.right, out);
    }
    public List<E> postorder() {
        List<E> out = new ArrayList<>(); postorder(root, out); return List.copyOf(out);
    }
    private static <E> void postorder(Node<E> x, List<E> out) {
        if (x == null) return;
        postorder(x.left, out); postorder(x.right, out); out.add(x.data);
    }
    public List<E> levelOrder() {
        if (root == null) return List.of();
        List<E> out = new ArrayList<>();
        Queue<Node<E>> q = new ArrayDeque<>(); q.add(root);
        while (!q.isEmpty()) {
            Node<E> x = q.remove(); out.add(x.data);
            if (x.left != null) q.add(x.left);
            if (x.right != null) q.add(x.right);
        }
        return List.copyOf(out);
    }
