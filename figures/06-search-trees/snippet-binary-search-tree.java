    private static final class Node {
        int key; Node left, right, parent;
        Node(int key) { this.key = key; }
    }
    private Node root;
    private int size;
    public int size() { return size; }
    private Node find(int key) {
        Node x=root;
        while(x!=null && x.key!=key) x=key<x.key?x.left:x.right;
        return x;
    }
    public boolean contains(int key) { return find(key)!=null; }
    public boolean insert(int key) {
        Node y=null,x=root;
        while(x!=null){y=x;if(key==x.key)return false;x=key<x.key?x.left:x.right;}
        Node z=new Node(key);z.parent=y;
        if(y==null)root=z;else if(key<y.key)y.left=z;else y.right=z;
        size++;return true;
    }
    private static Node minimum(Node x){if(x==null)return null;while(x.left!=null)x=x.left;return x;}
    private static Node maximum(Node x){if(x==null)return null;while(x.right!=null)x=x.right;return x;}
    public OptionalInt minimum(){Node x=minimum(root);return x==null?OptionalInt.empty():OptionalInt.of(x.key);}
    public OptionalInt maximum(){Node x=maximum(root);return x==null?OptionalInt.empty():OptionalInt.of(x.key);}
    private static Node successor(Node x){
        if(x.right!=null)return minimum(x.right);
        Node y=x.parent;while(y!=null&&x==y.right){x=y;y=y.parent;}return y;
    }
    private static Node predecessor(Node x){
        if(x.left!=null)return maximum(x.left);
        Node y=x.parent;while(y!=null&&x==y.left){x=y;y=y.parent;}return y;
    }
    public OptionalInt successor(int key){Node x=find(key);if(x==null)return OptionalInt.empty();Node y=successor(x);return y==null?OptionalInt.empty():OptionalInt.of(y.key);}
    public OptionalInt predecessor(int key){Node x=find(key);if(x==null)return OptionalInt.empty();Node y=predecessor(x);return y==null?OptionalInt.empty():OptionalInt.of(y.key);}
    private void transplant(Node u,Node v){
        if(u.parent==null)root=v;else if(u==u.parent.left)u.parent.left=v;else u.parent.right=v;
        if(v!=null)v.parent=u.parent;
    }
    public boolean delete(int key){
        Node z=find(key);if(z==null)return false;
        if(z.left==null)transplant(z,z.right);
        else if(z.right==null)transplant(z,z.left);
        else{Node y=minimum(z.right);if(y.parent!=z){transplant(y,y.right);y.right=z.right;y.right.parent=y;}transplant(z,y);y.left=z.left;y.left.parent=y;}
        size--;return true;
    }
    public List<Integer> inorder(){List<Integer>o=new ArrayList<>();inorder(root,o);return List.copyOf(o);}
    private static void inorder(Node x,List<Integer>o){if(x!=null){inorder(x.left,o);o.add(x.key);inorder(x.right,o);}}
