#include "state_space_search.h"
#include <stdio.h>

int main(void) {
    /* A-B-C-D-A cycle plus A-C diagonal, matching the lecture's own example. */
    const unsigned char adjacency[16] = {
        0,1,1,1,
        1,0,1,0,
        1,1,0,1,
        1,0,1,0,
    };
    int colors[4];
    if (ss_color_graph(adjacency, 4, 3, colors) != SS_OK) return 1;
    printf("colors: %d,%d,%d,%d\n", colors[0], colors[1], colors[2], colors[3]);
    return 0;
}
