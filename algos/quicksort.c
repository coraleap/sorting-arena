#include <stdio.h>
#include <stdbool.h>

void quickSort_general (int* array, int l_ind, int r_ind, 
    int (*findPivot)(int*, int, int), int (*partitionFunc)(int*, int, int, int),
    int minLength, bool hasFallback, int maxDepth, void (*fallbackAlgorithm)(int*, int, int)
    ) {

        if (r_ind - l_ind < minLength) {
            return;
        }

        if (hasFallback && maxDepth < 1) {
            (*fallbackAlgorithm)(array, l_ind, r_ind);
            return;
        }

        int pivot = (*findPivot)(array, l_ind, r_ind);

        int splitter = (*partitionFunc)(array, l_ind, r_ind, pivot);

        quickSort_general(array, l_ind, splitter, findPivot, partitionFunc, minLength, hasFallback, maxDepth - 1, fallbackAlgorithm);
        quickSort_general(array, splitter, r_ind, findPivot, partitionFunc, minLength, hasFallback, maxDepth - 1, fallbackAlgorithm);
}

void swap_two_inds(int* arr, int ind1, int ind2) {
    int buffer = arr[ind1];
    arr[ind1] = arr[ind2];
    arr[ind2] = buffer;
}

int select_leftmost(int *arr, int l_ind, int r_ind) {
    return arr[l_ind];
}

int find_median(int *arr, int l_ind, int r_ind) {

}

int LL_pointers (int *arr, int l_ind, int r_ind, int pivot_value) {
    int l_pointer = l_ind;
    int r_pointer = l_ind;
    while (r_pointer < r_ind - 1) {
        r_pointer++;
        if (arr[r_pointer] <= pivot_value) {
            swap_two_inds(arr, ++l_pointer, r_pointer);
        }
    }
    return l_pointer;
}

int LL_pointers_branchless (int *arr, int l_ind, int r_ind, int pivot_value) {
    int l_pointer = l_ind;
    int r_pointer = l_ind;
    while (r_pointer < r_ind - 1) {
        r_pointer++;
        swap_two_inds(arr, l_pointer + 1, r_pointer);
        l_pointer += (arr[r_pointer] <= pivot_value);
    }
    return l_pointer;
}

int LR_pointers (int *arr, int l_ind, int r_ind, int pivot_value) {
    int l_pointer = l_ind;
    int r_pointer = r_ind;

    while (l_pointer < r_pointer) {
        if (arr[l_pointer] > pivot_value) {
            swap_two_inds(arr, l_pointer, --r_pointer);
        }
        else {
            l_pointer++;
        }
    }
    return l_pointer;
}

void no_fallback(int* arr, int ind1, int ind2) {
    
}

void quickSort_LR(int* array, int length) {
    quickSort_general(array, 0, length, select_leftmost, LR_pointers, 2, false, 0, no_fallback);
}

void quickSort_LL(int* array, int length) {
    quickSort_general(array, 0, length, select_leftmost, LL_pointers, 2, false, 0, no_fallback);
}

void quickSort_LL_branchless(int* array, int length) {
    quickSort_general(array, 0, length, select_leftmost, LL_pointers_branchless, 2, false, 0, no_fallback);
}

