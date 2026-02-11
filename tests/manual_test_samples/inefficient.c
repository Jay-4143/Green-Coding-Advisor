
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

void extremely_inefficient_c() {
    printf("Running inefficient C code...\n");
    clock_t start = clock();
    
    // 1. Nested loops O(N^2) (Pattern: nested loops)
    // Metric: Quadratic complexity
    int n = 10000;
    long long sum = 0;
    
    // Inefficient: could be O(N) or O(1) mathematically
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            sum += (i * j) % 5;
        }
    }
    
    // 2. Allocation inside loop (Pattern: malloc in loop)
    // Metric: System call overhead, fragmentation
    for (int i = 0; i < 5000; i++) {
        // Inefficient: repeated small allocations
        int *ptr = (int *)malloc(sizeof(int) * 100);
        if (ptr) {
            // Do some work
            for (int k = 0; k < 100; k++) ptr[k] = k;
            free(ptr);
        }
    }
    
    // 3. Redundant Calculations (Pattern: calculation in loop)
    // Metric: Wasted CPU cycles
    double result = 0.0;
    for (int i = 0; i < 1000000; i++) {
        // Inefficient: invariant calculation inside loop 
        // (Compiler might optimize this out, but it's bad practice)
        double invariant = 3.14159 * 2.71828 / 1.414;
        result += i * invariant;
    }
    
    // 4. String Copying in Loop (Pattern: strcpy/strcat in loop)
    char buffer[10000] = "";
    for (int i = 0; i < 1000; i++) {
        // Inefficient: traversing string repeatedly (Shlemiel the Painter's algorithm)
        strcat(buffer, "a");
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Inefficient C finished in %f seconds\n", time_spent);
}

int main() {
    extremely_inefficient_c();
    return 0;
}
