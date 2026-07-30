    private static final boolean RED=true, BLACK=false;
    private final Node nil=new Node(0,BLACK);
    private Node root=nil;
    private int size;

    private final class Node {
        int key; boolean color; Node left,right,parent;
        Node(int key,boolean color){this.key=key;this.color=color;}
    }
    public RedBlackTree(){nil.left=nil.right=nil.parent=nil;}
    private Node find(int key){Node x=root;while(x!=nil&&x.key!=key)x=key<x.key?x.left:x.right;return x;}
    public boolean contains(int key){return find(key)!=nil;}
    public int size(){return size;}

    public boolean insert(int key){
        Node y=nil,x=root;
        while(x!=nil){y=x;if(key==x.key)return false;x=key<x.key?x.left:x.right;}
        Node z=new Node(key,RED);z.left=z.right=nil;z.parent=y;
        if(y==nil)root=z;else if(key<y.key)y.left=z;else y.right=z;
        size++;insertFixup(z);return true;
    }
    private void insertFixup(Node z){
        while(z.parent.color==RED){
            if(z.parent==z.parent.parent.left){
                Node u=z.parent.parent.right;
                if(u.color==RED){z.parent.color=BLACK;u.color=BLACK;z.parent.parent.color=RED;z=z.parent.parent;}
                else{if(z==z.parent.right){z=z.parent;rotateLeft(z);}z.parent.color=BLACK;z.parent.parent.color=RED;rotateRight(z.parent.parent);}
            }else{
                Node u=z.parent.parent.left;
                if(u.color==RED){z.parent.color=BLACK;u.color=BLACK;z.parent.parent.color=RED;z=z.parent.parent;}
                else{if(z==z.parent.left){z=z.parent;rotateRight(z);}z.parent.color=BLACK;z.parent.parent.color=RED;rotateLeft(z.parent.parent);}
            }
        }
        root.color=BLACK;root.parent=nil;
    }
    private void rotateLeft(Node x){
        Node y=x.right;x.right=y.left;if(y.left!=nil)y.left.parent=x;
        y.parent=x.parent;if(x.parent==nil)root=y;else if(x==x.parent.left)x.parent.left=y;else x.parent.right=y;
        y.left=x;x.parent=y;
    }
    private void rotateRight(Node y){
        Node x=y.left;y.left=x.right;if(x.right!=nil)x.right.parent=y;
        x.parent=y.parent;if(y.parent==nil)root=x;else if(y==y.parent.left)y.parent.left=x;else y.parent.right=x;
        x.right=y;y.parent=x;
    }
    private Node minimum(Node x){while(x.left!=nil)x=x.left;return x;}
    private void transplant(Node u,Node v){
        if(u.parent==nil)root=v;else if(u==u.parent.left)u.parent.left=v;else u.parent.right=v;
        v.parent=u.parent;
    }
    public boolean delete(int key){
        Node z=find(key);if(z==nil)return false;
        Node y=z,x;boolean original=y.color;
        if(z.left==nil){x=z.right;transplant(z,z.right);}
        else if(z.right==nil){x=z.left;transplant(z,z.left);}
        else{
            y=minimum(z.right);original=y.color;x=y.right;
            if(y.parent==z)x.parent=y;
            else{transplant(y,y.right);y.right=z.right;y.right.parent=y;}
            transplant(z,y);y.left=z.left;y.left.parent=y;y.color=z.color;
        }
        size--;if(original==BLACK)deleteFixup(x);
        if(root!=nil)root.parent=nil;else nil.parent=nil;
        return true;
    }
    private void deleteFixup(Node x){
        while(x!=root&&x.color==BLACK){
            if(x==x.parent.left){
                Node w=x.parent.right;
                if(w.color==RED){w.color=BLACK;x.parent.color=RED;rotateLeft(x.parent);w=x.parent.right;}
                if(w.left.color==BLACK&&w.right.color==BLACK){w.color=RED;x=x.parent;}
                else{
                    if(w.right.color==BLACK){w.left.color=BLACK;w.color=RED;rotateRight(w);w=x.parent.right;}
                    w.color=x.parent.color;x.parent.color=BLACK;w.right.color=BLACK;rotateLeft(x.parent);x=root;
                }
            }else{
                Node w=x.parent.left;
                if(w.color==RED){w.color=BLACK;x.parent.color=RED;rotateRight(x.parent);w=x.parent.left;}
                if(w.right.color==BLACK&&w.left.color==BLACK){w.color=RED;x=x.parent;}
                else{
                    if(w.left.color==BLACK){w.right.color=BLACK;w.color=RED;rotateLeft(w);w=x.parent.left;}
                    w.color=x.parent.color;x.parent.color=BLACK;w.left.color=BLACK;rotateRight(x.parent);x=root;
                }
            }
        }
        x.color=BLACK;
    }
    public List<Integer> inorder(){List<Integer>o=new ArrayList<>();inorder(root,o);return List.copyOf(o);}
    private void inorder(Node x,List<Integer>o){if(x!=nil){inorder(x.left,o);o.add(x.key);inorder(x.right,o);}}
