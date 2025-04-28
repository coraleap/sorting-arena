#include <stdio.h>

/*
Heap Sort coded by myself for 6.1903
*/

void swap_two_inds(int* arr, int ind1, int ind2) {
    int buffer = arr[ind1];
    arr[ind1] = arr[ind2];
    arr[ind2] = buffer;
}

void sift_down(int* arr, int heap_length, int ind) {
    if (ind * 2 + 2 < heap_length) {
        int child_ind_1 = 2 * ind + 1;
        int child_ind_2 = 2 * ind + 2;
        int larger_child = 2 * ind + 1 + (arr[child_ind_2] > arr[child_ind_1]);
        if (arr[ind] < arr[larger_child]) {
            swap_two_inds(arr, ind, larger_child);
            sift_down(arr, heap_length, larger_child);
        }
    }
    else if (ind * 2 + 2 == heap_length) {
        int child_ind = 2 * ind + 1;
        if (arr[ind] < arr[child_ind]) {
            swap_two_inds(arr, ind, child_ind);
        }
    }
}

void heapify(int* arr, int array_len) {
    // We heapify into a maxheap tree, with each parent larger than children.
    for (int i = (array_len - 1) / 2; i >= 0; i--) {
        sift_down(arr, array_len, i);
    }
}

void array_sort(int* scores, int array_len){
    heapify(scores, array_len);
    int heap_length = array_len;
    while (heap_length > 0) {
        swap_two_inds(scores, 0, heap_length - 1);
        heap_length--;
        sift_down(scores, heap_length, 0);
    }
}