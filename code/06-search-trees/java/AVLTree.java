import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** lecture-notes/code/lecture06/java/AVLTree.java와 동일(verbatim).
 * Distinct int keys. Empty height=-1, leaf height=0, BF=left-right. */
public final class AVLTree {
    // snippet:avl-tree:start
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
    // snippet:avl-tree:end
    public boolean delete(int k){if(!contains(k))return false;root=delete(root,k);size--;return true;}
    private static Node delete(Node x,int k){
        if(k<x.key)x.left=delete(x.left,k);else if(k>x.key)x.right=delete(x.right,k);
        else{if(x.left==null)return x.right;if(x.right==null)return x.left;Node y=x.right;while(y.left!=null)y=y.left;x.key=y.key;x.right=delete(x.right,y.key);}
        return rebalance(x);
    }

    private static String join(List<Integer> a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.size(); i++) { if (i > 0) sb.append(','); sb.append(a.get(i)); }
        return sb.toString();
    }

    public static void main(String[] args) {
        Map<String, int[]> cases = new LinkedHashMap<>();
        cases.put("LL", new int[] {30, 20, 10});
        cases.put("RR", new int[] {10, 20, 30});
        cases.put("LR", new int[] {30, 10, 20});
        cases.put("RL", new int[] {10, 30, 20});
        for (Map.Entry<String, int[]> e : cases.entrySet()) {
            AVLTree t = new AVLTree();
            for (int k : e.getValue()) t.insert(k);
            System.out.println(e.getKey() + " inorder: " + join(t.inorder()));
            System.out.println(e.getKey() + " height: " + t.height());
        }
        AVLTree big = new AVLTree();
        for (int i = 0; i < 15; i++) big.insert(i);
        System.out.println("sequential15 height: " + big.height());
        System.out.println("sequential15 inorder: " + join(big.inorder()));
    }
}
