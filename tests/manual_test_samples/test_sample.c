
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void inefficient_code() {
    printf("Running inefficient C code...\n");
    clock_t start = clock();
    
    // 1. Inefficient loop with redundant calculations
    int sum = 0;
    for (int i = 0; i < 100000; i++) {
        for (int j = 0; j < 100; j++) {
            sum += i * j;
        }
    }
    
    // 2. Multiple small allocations
    for (int i = 0; i < 1000; i++) {
        int* ptr = (int*)malloc(sizeof(int));
        *ptr = i;
        free(ptr);
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Inefficient C code took: %f seconds\n", time_spent);
}

void efficient_code() {
    printf("Running efficient C code...\n");
    clock_t start = clock();
    
    // 1. Optimized loop (hoisting, unrolling - though compiler does this too)
    long long sum = 0;
    for (int i = 0; i < 100000; i++) {
        // Mathematical formula for sum of 0..99 is 99*100/2 = 4950
        sum += i * 4950;
    }
    
    // 2. Batch allocation (if needed) or stack allocation
    int buffer[1000];
    for (int i = 0; i < 1000; i++) {
        buffer[i] = i;
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Efficient C code took: %f seconds\n", time_spent);
}

int main() {
    inefficient_code();
    efficient_code();
    return 0;
}
