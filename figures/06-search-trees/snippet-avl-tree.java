    private static final class Node {int key,height;Node left,right;Node(int k){key=k;}}
    private Node root;private int size;
    private static int h(Node x){return x==null?-1:x.height;}
    private static void update(Node x){x.height=1+Math.max(h(x.left),h(x.right));}
    private static int bf(Node x){return h(x.left)-h(x.right);}
    public boolean contains(int k){Node x=root;while(x!=null){if(k==x.key)return true;x=k<x.key?x.left:x.right;}return false;}
    public boolean insert(int k){if(contains(k))return false;root=insert(root,k);size++;return true;}
    private static Node insert(Node x,int k){if(x==null)return new Node(k);if(k<x.key)x.left=insert(x.left,k);else x.right=insert(x.right,k);return rebalance(x);}
    private static Node rebalance(Node x){update(x);if(bf(x)>1){if(bf(x.left)<0)x.left=left(x.left);return right(x);}if(bf(x)<-1){if(bf(x.right)>0)x.right=right(x.right);return left(x);}return x;}
    private static Node right(Node y){Node x=y.left,b=x.right;x.right=y;y.left=b;update(y);update(x);return x;}
    private static Node left(Node x){Node y=x.right,b=y.left;y.left=x;x.right=b;update(x);update(y);return y;}
    public List<Integer> inorder(){List<Integer>o=new ArrayList<>();inorder(root,o);return List.copyOf(o);}
    private static void inorder(Node x,List<Integer>o){if(x!=null){inorder(x.left,o);o.add(x.key);inorder(x.right,o);}}
    public int height(){return h(root);}
