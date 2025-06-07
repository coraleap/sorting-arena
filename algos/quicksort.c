#include <stdio.h>
#include <stdbool.h>

void insertionSort (int* array, int l_ind, int r_ind) {
    for (int i = l_ind; i < r_ind; i++) {
        int temp = array[i];
        int j = i;
        for (;j > l_ind && array[j - 1] > temp; j--) {
            array[j] = array[j - 1]; // Inserting j into list
        }
        array[j] = temp;
    }
}

void swap_two_inds(int* arr, int ind1, int ind2) {
    int buffer = arr[ind1];
    arr[ind1] = arr[ind2];
    arr[ind2] = buffer;
}

void sift_down(int* arr, int l_ind, int heap_end, int ind) {
    int diff = ind - l_ind;
    if (diff * 2 + 2 < heap_end - l_ind) {
        int child_ind_1 = 2 * diff + l_ind + 1;
        int child_ind_2 = child_ind_1 + 1;
        int larger_child = 2 * diff + 1 + (arr[child_ind_2] > arr[child_ind_1]);
        if (arr[ind] < arr[larger_child]) {
            swap_two_inds(arr, ind, larger_child);
            sift_down(arr, l_ind, heap_end, larger_child);
        }
    }
    else if (diff * 2 + 2 == heap_end - l_ind) {
        int child_ind = 2 * diff + l_ind + 1;
        if (arr[ind] < arr[child_ind]) {
            swap_two_inds(arr, ind, child_ind);
        }
    }
}

void heapify(int* arr, int l_ind, int heap_end) {
    // We heapify into a maxheap tree, with each parent larger than children.
    for (int i = (heap_end + l_ind - 1) / 2; i >= l_ind; i--) {
        sift_down(arr, l_ind, heap_end, i);
    }
}

void heap_sort(int* scores, int l_ind, int r_ind){
    heapify(scores, l_ind, r_ind);
    int heap_end = r_ind;
    while (heap_end > l_ind) {
        swap_two_inds(scores, l_ind, heap_end - 1);
        heap_end--;
        sift_down(scores, l_ind, heap_end, l_ind);
    }
}

void quickSort_general (int* array, int l_ind, int r_ind, 
    int (*findPivot)(int*, int, int), int (*partitionFunc)(int*, int, int, int, bool),
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

        int splitter = (*partitionFunc)(array, l_ind, r_ind, pivot, 1);
        int lsplitter = splitter;

        if (splitter == r_ind) {
            lsplitter = (*partitionFunc)(array, l_ind, splitter, pivot, 0);
        }

        quickSort_general(array, l_ind, lsplitter, findPivot, partitionFunc, minLength, hasFallback, maxDepth - 1, fallbackAlgorithm);
        quickSort_general(array, splitter, r_ind, findPivot, partitionFunc, minLength, hasFallback, maxDepth - 1, fallbackAlgorithm);
}




int select_leftmost(int *arr, int l_ind, int r_ind) {
    return arr[l_ind];
}

int quickselect_small(int *arr, int l_ind, int r_ind, int t_ind) {
    insertionSort(arr, l_ind, r_ind);
    return arr[t_ind];
}

int find_min(int *arr, int l_ind, int r_ind) {
    int current_min = arr[l_ind];
    for (int i = l_ind + 1; i < r_ind; i++) {
        if (arr[i] < current_min) {
            current_min = arr[i];
        }
    }
    return current_min;
}

int find_max(int *arr, int l_ind, int r_ind) {
    int current_max = arr[l_ind];
    for (int i = l_ind + 1; i < r_ind; i++) {
        if (arr[i] > current_max) {
            current_max = arr[i];
        }
    }
    return current_max;
}


int three_median(int* arr, int l_ind, int r_ind) {
    int left = arr[l_ind];
    int right = arr[r_ind];
    int middle = arr[(l_ind + r_ind) / 2];

    if ((left <= middle) ^ (right <= middle)) {
        return middle;
    }
    else if ((middle <= left) ^ (right <= left)) {
        return left;
    }
    else {
        return right;
    }
}

int LL_pointers (int *arr, int l_ind, int r_ind, int pivot_value, bool partLeft) {
    int l_pointer = l_ind;
    int r_pointer = l_ind;

    if (partLeft) {
        while (r_pointer < r_ind) {
            if (arr[r_pointer] <= pivot_value) {
                swap_two_inds(arr, l_pointer++, r_pointer);
            }
            r_pointer++;
        }
    }
    else {
        while (r_pointer < r_ind) {
            if (arr[r_pointer] < pivot_value) {
                swap_two_inds(arr, l_pointer++, r_pointer);
            }
            r_pointer++;
        }
    }

    return l_pointer;
}

int LL_pointers_branchless (int *arr, int l_ind, int r_ind, int pivot_value, bool partLeft) {

    
    int l_pointer = l_ind;
    int r_pointer = l_ind;

    if (partLeft){
        while (r_pointer < r_ind) {
            r_pointer++;
            swap_two_inds(arr, l_pointer, r_pointer);
            l_pointer += (arr[l_pointer] <= pivot_value);
        }
    }
    else {
        while (r_pointer < r_ind) {
            r_pointer++;
            swap_two_inds(arr, l_pointer, r_pointer);
            l_pointer += (arr[l_pointer] < pivot_value);
        }
    }
    return l_pointer;
}

int LR_pointers (int *arr, int l_ind, int r_ind, int pivot_value, bool partLeft) {
    int l_pointer = l_ind;
    int r_pointer = r_ind;

    if (partLeft) {
        while (l_pointer < r_pointer) {
            if (arr[l_pointer] > pivot_value) {
                swap_two_inds(arr, l_pointer, --r_pointer);
            }
            else {
                l_pointer++;
            }
        }
    }
    else {
        while (l_pointer < r_pointer) {
            if (arr[l_pointer] >= pivot_value) {
                swap_two_inds(arr, l_pointer, --r_pointer);
            }
            else {
                l_pointer++;
            }
        }
    }
    return l_pointer;
}

int quick_select(int *arr, int l_ind, int r_ind, int t_ind) {
    if ((r_ind - l_ind) < 16) {
        return quickselect_small(arr, l_ind, r_ind, t_ind);
    }

    int numGroups = (r_ind - l_ind) / 5;
    if (!(numGroups % 2)) numGroups--;

    int medians[numGroups];

    for (int i = 0; i < numGroups; i++) {
        int offset = 5 * i + l_ind;
        medians[i] = quickselect_small(arr, offset, offset + 5, offset + 2);
    }

    int median_of_medians = quick_select(medians, 0, numGroups, numGroups / 2);

    int dividing_line = LR_pointers(arr, l_ind, r_ind, median_of_medians, true);
    if (5 * (l_ind - dividing_line) / (r_ind - l_ind) > 4) {
        int dividing_line_l = LR_pointers(arr, l_ind, r_ind, median_of_medians, false);

        if (t_ind >= dividing_line_l && t_ind < dividing_line) {
            return median_of_medians;
        }

        dividing_line = (dividing_line + dividing_line_l) / 2;
    }

    if (t_ind >= dividing_line) {
        return quick_select(arr, dividing_line, r_ind, t_ind);
    }
    else {
        return quick_select(arr, l_ind, dividing_line, t_ind);
    }
}

int median_finder(int *arr, int l_ind, int r_ind) {
    return quick_select(arr, l_ind, r_ind, (l_ind + r_ind) / 2);
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










void intro_sort_onemedian(int* array, int length, int minlen) {
    int digits = 0;
    int tracker = length;
    while (tracker > 0) {
        tracker = tracker >> 1;
        digits++;
    }
    quickSort_general(array, 0, length, select_leftmost, LR_pointers, minlen, true, 3 * digits + 3, heap_sort);
    insertionSort(array, 0, length);
}

void intro_sort_threemedian(int* array, int length, int minlen) {
    int digits = 0;
    int tracker = length;
    while (tracker > 0) {
        tracker = tracker >> 1;
        digits++;
    }
    quickSort_general(array, 0, length, three_median, LR_pointers, minlen, true, 3 * digits + 3, heap_sort);
    insertionSort(array, 0, length);
}

void quick_MoMpivot(int* array, int length) {
    quickSort_general(array, 0, length, median_finder, LR_pointers, 2, false, 0, no_fallback);
}

int main () {
    int test1[1000];
    for (int i = 0; i < 1000; i++) {
        test1[i] = i;
    }

    // quick_MoMpivot(test1, 100);
    int med = median_finder(test1, 0, 1000);
    printf("%d", med);
    return 0;
}
    
