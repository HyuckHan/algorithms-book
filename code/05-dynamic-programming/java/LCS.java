public final class LCS {
    private LCS() {}

    // Bottom-up, tie-up backtracking. Reused verbatim from
    // lecture-notes/code/lecture05/java/LCS.java (solve), renamed to match
    // this chapter's pseudocode block name ("LCS Bottom-Up"). Theta(m*n)
    // time/table space.
    // snippet:lcs-bottom-up:start
    public static String lcsBottomUp(String x,String y){
        if(x==null||y==null)throw new IllegalArgumentException();
        int m=x.length(),n=y.length();int[][] d=new int[m+1][n+1];
        for(int i=1;i<=m;i++)for(int j=1;j<=n;j++)d[i][j]=x.charAt(i-1)==y.charAt(j-1)?d[i-1][j-1]+1:Math.max(d[i-1][j],d[i][j-1]);
        StringBuilder s=new StringBuilder();int i=m,j=n;
        while(i>0&&j>0){if(x.charAt(i-1)==y.charAt(j-1)){s.append(x.charAt(i-1));i--;j--;}else if(d[i-1][j]>=d[i][j-1])i--;else j--;}
        return s.reverse().toString();
    }
    // snippet:lcs-bottom-up:end

    public static void main(String[] args) {
        String x = "ABCBDAB", y = "BDCABA";
        String s = lcsBottomUp(x, y);
        System.out.println("X: " + x);
        System.out.println("Y: " + y);
        System.out.println("lcs: " + s);
        System.out.println("length: " + s.length());
    }
}
