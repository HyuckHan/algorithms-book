import java.util.Random;

public final class RandomizedSelect {
    // snippet:randomized-select:start
    /** 강의노트 원본의 select를 그대로
     * 옮긴 것이다. 무작위인 것은 내부 pivot 선택뿐이고, 결과는 어떤 pivot을
     * 뽑든 항상 정확한 rank번째 값이다. rank는 0-based(0..n-1). */
    static int randomizedSelect(int[] a, int rank, Random random) {
        int lo = 0, hi = a.length;
        while (true) {
            if (hi - lo == 1) return a[lo];
            int pivot = a[lo + random.nextInt(hi - lo)];
            int[] equal = partition3(a, lo, hi, pivot);
            if (rank < equal[0]) hi = equal[0];
            else if (rank >= equal[1]) lo = equal[1];
            else return pivot;
        }
    }

    /** [lt, gt) 구간이 pivot과 같다. */
    private static int[] partition3(int[] a, int lo, int hi, int pivot) {
        int lt = lo, scan = lo, gt = hi;
        while (scan < gt) {
            if (a[scan] < pivot) swap(a, lt++, scan++);
            else if (a[scan] > pivot) swap(a, scan, --gt);
            else scan++;
        }
        return new int[] {lt, gt};
    }

    private static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
    // snippet:randomized-select:end

    public static void main(String[] args) {
        int[] data = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
        System.out.println("input: " + toCsv(data));
        Random random = new Random(20260729L);
        for (int rank : new int[] {1, 6}) {
            System.out.println("rank: " + rank);
            System.out.println("result: " + randomizedSelect(data.clone(), rank, random));
        }
    }

    private static String toCsv(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
