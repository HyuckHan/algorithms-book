    public static Result minPathBottomUp(long[][] a) {
        if(a==null||a.length==0||a[0]==null||a[0].length==0)throw new IllegalArgumentException();
        int r=a.length,c=a[0].length;for(long[] row:a)if(row==null||row.length!=c)throw new IllegalArgumentException();
        long[][] d=new long[r][c];byte[][] p=new byte[r][c];d[0][0]=a[0][0];
        for(int j=1;j<c;j++){d[0][j]=Math.addExact(d[0][j-1],a[0][j]);p[0][j]=2;}
        for(int i=1;i<r;i++){d[i][0]=Math.addExact(d[i-1][0],a[i][0]);p[i][0]=1;}
        for(int i=1;i<r;i++)for(int j=1;j<c;j++){if(d[i-1][j]<=d[i][j-1]){d[i][j]=Math.addExact(d[i-1][j],a[i][j]);p[i][j]=1;}else{d[i][j]=Math.addExact(d[i][j-1],a[i][j]);p[i][j]=2;}}
        int[][] path=new int[r+c-1][2];int i=r-1,j=c-1;
        for(int k=path.length-1;k>=0;k--){path[k][0]=i;path[k][1]=j;if(i==0&&j==0)break;if(p[i][j]==1)i--;else j--;}
        return new Result(d[r-1][c-1],path);
    }
