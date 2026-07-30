#include <stdio.h>

// snippet:recursive-binary-search:start
/* Recursive Binary Search. Base case: begin > end (empty interval, -1, no
 * further call). Recursive case: narrow to one inclusive half
 * [begin,mid-1] or [mid+1,end], progress measure end-begin strictly
 * decreasing. Max call-stack depth is Theta(log n). mid uses the
 * overflow-safe `begin + (end-begin)/2` form. */
int bsearch(int A[], int x, int begin, int end) {
  if (begin > end) return -1;
  int mid = begin + (end - begin) / 2;
  if (A[mid] == x) return mid;
  if (x < A[mid]) return bsearch(A,x,begin,mid-1);
  return bsearch(A,x,mid+1,end);
}
// snippet:recursive-binary-search:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {2, 5, 8, 12, 16, 23, 38};
    int n = sizeof(data) / sizeof(data[0]);
    int x = 16;
    print_array("input", data, n);
    printf("x: %d\n", x);
    printf("bsearch: %d\n", bsearch(data, x, 0, n - 1));
    return 0;
}
