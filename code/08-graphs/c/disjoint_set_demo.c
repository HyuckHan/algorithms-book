#include "graph.h"
#include <stdio.h>

int main(void) {
    DisjointSet d = {0};
    dsu_init(&d, 4);
    const char *name = "ABCD";
    size_t edges[][2] = {{0,1},{2,3},{1,2},{0,3}};
    for (size_t i = 0; i < 4; i++) {
        bool accepted = dsu_union(&d, edges[i][0], edges[i][1]);
        printf("%c%c: %s\n", name[edges[i][0]], name[edges[i][1]], accepted ? "accept" : "reject");
    }
    printf("components: ");
    for (size_t root = 0; root < 4; root++) {
        bool any = false;
        for (size_t v = 0; v < 4; v++) if (dsu_find(&d, v) == root) {
            printf(any ? ",%c" : "{%c", name[v]);
            any = true;
        }
        if (any) printf("}");
    }
    printf("\n");
    dsu_destroy(&d);
    return 0;
}
