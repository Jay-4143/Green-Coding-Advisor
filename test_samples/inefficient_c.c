/*
 * Inefficient C Code — For Green Coding Advisor Testing
 * Contains anti-patterns that the optimizer should detect.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 1. strcat in loop (O(n²) due to repeated strlen) */
void build_message(char *dest, const char *words[], int count) {
    dest[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(dest, words[i]);
        strcat(dest, " ");
    }
}

/* 2. malloc without free (memory leak) */
int* create_squares(int n) {
    int *squares = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        squares[i] = i * i;
    }
    return squares;
    /* Memory is never freed by caller */
}

/* 3. Bubble sort — O(n²) instead of qsort */
void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

/* 4. Repeated strlen calls in loop */
void count_chars(const char *str, int *letter_count, int *digit_count) {
    *letter_count = 0;
    *digit_count = 0;
    for (int i = 0; i < strlen(str); i++) {
        if (str[i] >= 'a' && str[i] <= 'z') {
            (*letter_count)++;
        } else if (str[i] >= '0' && str[i] <= '9') {
            (*digit_count)++;
        }
    }
}

/* 5. Manual array copy instead of memcpy */
void copy_array(int *dest, const int *src, int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}

/* 6. Nested loop for search — O(n²) */
int find_common_count(int *a, int na, int *b, int nb) {
    int count = 0;
    for (int i = 0; i < na; i++) {
        for (int j = 0; j < nb; j++) {
            if (a[i] == b[j]) {
                count++;
                break;
            }
        }
    }
    return count;
}

int main() {
    /* Test strcat in loop */
    char message[1024];
    const char *words[] = {"Green", "Coding", "Advisor", "Test"};
    build_message(message, words, 4);
    printf("Message: %s\n", message);

    /* Test bubble sort */
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);
    bubble_sort(arr, n);
    printf("Sorted: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    /* Test char counting */
    int letters, digits;
    count_chars("Hello123World456", &letters, &digits);
    printf("Letters: %d, Digits: %d\n", letters, digits);

    /* Test common elements */
    int a[] = {1, 2, 3, 4, 5};
    int b[] = {3, 4, 5, 6, 7};
    printf("Common: %d\n", find_common_count(a, 5, b, 5));

    return 0;
}
