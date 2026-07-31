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
