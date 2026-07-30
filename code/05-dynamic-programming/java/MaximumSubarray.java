public final class MaximumSubarray {
    public record Result(long sum, int start, int end) {}
    private MaximumSubarray() {}

    // All Theta(n^2) intervals, matching the "Brute Force" pseudocode
    // exactly. New for this book -- the canonical Java only has the
    // linear-time Kadane form.
    // snippet:max-subarray-brute-force:start
    public static Result maxSubarrayBruteForce(long[] a) {
        if (a == null || a.length == 0) throw new IllegalArgumentException();
        Result best = new Result(a[0], 0, 0);
        for (int i = 0; i < a.length; i++) {
            long sum = 0;
            for (int j = i; j < a.length; j++) {
                sum = Math.addExact(sum, a[j]);
                if (sum > best.sum()) best = new Result(sum, i, j);
            }
        }
        return best;
    }
    // snippet:max-subarray-brute-force:end

    private static int len(Result r){return r.end()-r.start()+1;}
    private static boolean better(Result a,Result b){return a.sum()>b.sum()||(a.sum()==b.sum()&&(len(a)<len(b)||(len(a)==len(b)&&a.start()<b.start())));}

    // bestEndingAt[i]/bestOverall (Kadane), matching the DP-template state
    // split. Reused verbatim from
    // lecture-notes/code/lecture05/java/MaximumSubarray.java (solve),
    // renamed to match this chapter's section heading. Nonempty, 0-based
    // inclusive interval. Theta(n) time, Theta(1) space.
    // snippet:max-subarray-kadane:start
    public static Result maxSubarrayKadane(long[] a){
        if(a==null||a.length==0)throw new IllegalArgumentException();
        Result ending=new Result(a[0],0,0),best=ending;
        for(int i=1;i<a.length;i++){Result extend=new Result(Math.addExact(ending.sum(),a[i]),ending.start(),i),restart=new Result(a[i],i,i);ending=better(restart,extend)?restart:extend;if(better(ending,best))best=ending;}
        return best;
    }
    // snippet:max-subarray-kadane:end

    public static void main(String[] args) {
        long[] a = {-2,1,-3,4,-1,2,1,-5,4};
        Result r1 = maxSubarrayBruteForce(a);
        Result r2 = maxSubarrayKadane(a);
        System.out.println("brute_force sum: " + r1.sum() + " start: " + r1.start() + " end: " + r1.end());
        System.out.println("kadane sum: " + r2.sum() + " start: " + r2.start() + " end: " + r2.end());
    }
}
