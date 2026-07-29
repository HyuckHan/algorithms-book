#include <assert.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *name;
    int quantity;
} Fruit;

static int compare_int(const void *pa, const void *pb) {
    int a = *(const int *)pa;
    int b = *(const int *)pb;
    return (a > b) - (a < b);
}

static int compare_fruit(const void *pa, const void *pb) {
    const Fruit *a = pa;
    const Fruit *b = pb;
    int by_quantity = (a->quantity > b->quantity)
                    - (a->quantity < b->quantity);
    return by_quantity != 0 ? by_quantity : strcmp(a->name, b->name);
}

static void assert_ints_sorted(const int *values, size_t n) {
    for (size_t i = 1; i < n; ++i) assert(values[i - 1] <= values[i]);
}

int main(void) {
    int values[] = {29, INT_MAX, 10, INT_MIN, 14, 10, 37, 13};
    Fruit fruits[] = {
        {"Orange", 5}, {"Banana", 3}, {"Apple", 5}, {"Apple", 5}
    };
    size_t value_count = sizeof values / sizeof values[0];
    size_t fruit_count = sizeof fruits / sizeof fruits[0];

    qsort(values, value_count, sizeof values[0], compare_int);
    qsort(fruits, fruit_count, sizeof fruits[0], compare_fruit);

    assert_ints_sorted(values, value_count);
    assert(values[0] == INT_MIN && values[value_count - 1] == INT_MAX);
    assert(fruits[0].quantity == 3);
    assert(strcmp(fruits[1].name, "Apple") == 0);
    assert(strcmp(fruits[2].name, "Apple") == 0);
    assert(strcmp(fruits[3].name, "Orange") == 0);

    puts("qsort_examples tests passed");
    return 0;
}
