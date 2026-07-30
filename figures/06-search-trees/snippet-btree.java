    private final class Node {
        final List<Integer> keys=new ArrayList<>();
        final List<Node> children=new ArrayList<>();
        boolean leaf;
        Node(boolean leaf){this.leaf=leaf;}
    }
    private final int t;
    private Node root=new Node(true);
    private int size;
    public BTree(int minimumDegree){if(minimumDegree<2)throw new IllegalArgumentException("t >= 2");t=minimumDegree;}
    public int size(){return size;}
    private static int lowerBound(List<Integer>a,int k){int i=0;while(i<a.size()&&a.get(i)<k)i++;return i;}
    public boolean contains(int k){return contains(root,k);}
    private boolean contains(Node x,int k){int i=lowerBound(x.keys,k);if(i<x.keys.size()&&x.keys.get(i)==k)return true;return !x.leaf&&contains(x.children.get(i),k);}
    public boolean insert(int k){
        if(contains(k))return false;
        if(root.keys.size()==2*t-1){Node s=new Node(false);s.children.add(root);splitChild(s,0);root=s;}
        insertNonFull(root,k);size++;return true;
    }
    private void insertNonFull(Node x,int k){
        int i=lowerBound(x.keys,k);
        if(x.leaf){x.keys.add(i,k);return;}
        if(x.children.get(i).keys.size()==2*t-1){splitChild(x,i);if(k>x.keys.get(i))i++;}
        insertNonFull(x.children.get(i),k);
    }
    private void splitChild(Node x,int i){
        Node y=x.children.get(i),z=new Node(y.leaf);
        int median=y.keys.get(t-1);
        for(int j=t;j<2*t-1;j++)z.keys.add(y.keys.get(j));
        while(y.keys.size()>t-1)y.keys.remove(y.keys.size()-1);
        if(!y.leaf){
            for(int j=t;j<2*t;j++)z.children.add(y.children.get(j));
            while(y.children.size()>t)y.children.remove(y.children.size()-1);
        }
        x.keys.add(i,median);x.children.add(i+1,z);
    }
    public boolean delete(int k){
        if(!contains(k))return false;
        delete(root,k);
        if(root.keys.isEmpty()&&!root.leaf)root=root.children.get(0);
        size--;return true;
    }
    private void delete(Node x,int k){
        int i=lowerBound(x.keys,k);
        if(i<x.keys.size()&&x.keys.get(i)==k){
            if(x.leaf)x.keys.remove(i);
            else if(x.children.get(i).keys.size()>=t){
                int pred=max(x.children.get(i));x.keys.set(i,pred);delete(x.children.get(i),pred);
            }else if(x.children.get(i+1).keys.size()>=t){
                int succ=min(x.children.get(i+1));x.keys.set(i,succ);delete(x.children.get(i+1),succ);
            }else{merge(x,i);delete(x.children.get(i),k);}
            return;
        }
        int child=i;
        if(x.children.get(child).keys.size()==t-1){
            if(child>0&&x.children.get(child-1).keys.size()>=t)borrowPrev(x,child);
            else if(child<x.children.size()-1&&x.children.get(child+1).keys.size()>=t)borrowNext(x,child);
            else{if(child<x.children.size()-1)merge(x,child);else{merge(x,child-1);child--;}}
        }
        delete(x.children.get(child),k);
    }
    private int min(Node x){while(!x.leaf)x=x.children.get(0);return x.keys.get(0);}
    private int max(Node x){while(!x.leaf)x=x.children.get(x.children.size()-1);return x.keys.get(x.keys.size()-1);}
    private void borrowPrev(Node x,int i){
        Node c=x.children.get(i),s=x.children.get(i-1);
        c.keys.add(0,x.keys.get(i-1));x.keys.set(i-1,s.keys.remove(s.keys.size()-1));
        if(!c.leaf)c.children.add(0,s.children.remove(s.children.size()-1));
    }
    private void borrowNext(Node x,int i){
        Node c=x.children.get(i),s=x.children.get(i+1);
        c.keys.add(x.keys.get(i));x.keys.set(i,s.keys.remove(0));
        if(!c.leaf)c.children.add(s.children.remove(0));
    }
    private void merge(Node x,int i){
        Node c=x.children.get(i),s=x.children.remove(i+1);
        c.keys.add(x.keys.remove(i));c.keys.addAll(s.keys);if(!c.leaf)c.children.addAll(s.children);
    }
    public List<Integer> inorder(){List<Integer>o=new ArrayList<>();inorder(root,o);return List.copyOf(o);}
    private void inorder(Node x,List<Integer>o){
        for(int i=0;i<x.keys.size();i++){if(!x.leaf)inorder(x.children.get(i),o);o.add(x.keys.get(i));}
        if(!x.leaf)inorder(x.children.get(x.keys.size()),o);
    }
