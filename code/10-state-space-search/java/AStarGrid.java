import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.PriorityQueue;

/** lecture-notes/code/lecture10/java/AStarGrid.java와 같은 정책(4-neighbor
 * unit-cost grid, Manhattan heuristic, stale-g-snapshot 검사, permanent
 * CLOSED, path reconstruction). */
public final class AStarGrid {
    public static final class Result {
        public List<int[]> path = new ArrayList<>();
        public int cost = Integer.MAX_VALUE;
        public int expanded;
        public int maxFrontier;
        public boolean goalDiscoveredBeforeExtraction;
        public boolean goalExtracted;
    }
    private static final class Entry implements Comparable<Entry> {
        final int r, c, g, f;
        Entry(int r, int c, int g, int f) { this.r=r; this.c=c; this.g=g; this.f=f; }
        public int compareTo(Entry o) {
            int x=Integer.compare(f,o.f); if(x!=0)return x;
            x=Integer.compare(g,o.g); if(x!=0)return x;
            x=Integer.compare(r,o.r); return x!=0?x:Integer.compare(c,o.c);
        }
    }
    private static final int[][] DIR={{-1,0},{0,-1},{0,1},{1,0}};

    // snippet:a-star:start
    public Result search(boolean[][] blocked, int sr, int sc, int gr, int gc, boolean zeroHeuristic) {
        validate(blocked, sr, sc, gr, gc);
        int rows=blocked.length, cols=blocked[0].length;
        int[][] g=new int[rows][cols], pr=new int[rows][cols], pc=new int[rows][cols];
        boolean[][] closed=new boolean[rows][cols];
        for(int[] row:g)Arrays.fill(row,Integer.MAX_VALUE);
        for(int[] row:pr)Arrays.fill(row,-1);
        for(int[] row:pc)Arrays.fill(row,-1);
        PriorityQueue<Entry> open=new PriorityQueue<>();
        g[sr][sc]=0; open.add(new Entry(sr,sc,0,h(sr,sc,gr,gc,zeroHeuristic)));
        Result out=new Result();
        while(!open.isEmpty()){
            out.maxFrontier=Math.max(out.maxFrontier,open.size());
            Entry e=open.remove();
            if(e.g!=g[e.r][e.c])continue;
            if(closed[e.r][e.c])continue;
            closed[e.r][e.c]=true;
            out.expanded++;
            if(e.r==gr&&e.c==gc){
                out.goalExtracted=true;
                out.cost=e.g;
                break;
            }
            for(int[] d:DIR){
                int nr=e.r+d[0],nc=e.c+d[1];
                if(nr<0||nr>=rows||nc<0||nc>=cols||blocked[nr][nc])continue;
                if(closed[nr][nc])continue;
                if(e.g==Integer.MAX_VALUE)continue;
                int ng=e.g+1;
                if(ng<g[nr][nc]){
                    g[nr][nc]=ng;pr[nr][nc]=e.r;pc[nr][nc]=e.c;
                    if(nr==gr&&nc==gc)out.goalDiscoveredBeforeExtraction=true;
                    open.add(new Entry(nr,nc,ng,ng+h(nr,nc,gr,gc,zeroHeuristic)));
                }
            }
        }
        if(out.cost!=Integer.MAX_VALUE){
            int r=gr,c=gc;
            while(r!=-1){out.path.add(new int[]{r,c});int nr=pr[r][c];c=pc[r][c];r=nr;}
            Collections.reverse(out.path);
        }
        return out;
    }
    private static int h(int r,int c,int gr,int gc,boolean zero){
        return zero?0:Math.abs(r-gr)+Math.abs(c-gc);
    }
    // snippet:a-star:end
    private static void validate(boolean[][] b,int sr,int sc,int gr,int gc){
        if(b==null||b.length==0||b[0].length==0)throw new IllegalArgumentException();
        int cols=b[0].length;for(boolean[] row:b)if(row==null||row.length!=cols)throw new IllegalArgumentException();
        if(sr<0||sr>=b.length||gr<0||gr>=b.length||sc<0||sc>=cols||gc<0||gc>=cols||b[sr][sc]||b[gr][gc])throw new IllegalArgumentException();
    }
}
