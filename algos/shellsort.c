#include <stdio.h>
#include <stdlib.h>

void shellSort_pass (int* array, int length, int gap) {
    for (int i = gap; i < length; i++) {
        int temp = array[i];
        int j = i;
        for (;j >= gap && array[j - gap] > temp; j -= gap) {
            array[j] = array[j - gap]; // Inserting j into list
        }
        array[j] = temp;
    }
}

void shellSort_dynamic (int* array, int length, int first_gap, int (*nextGap)(int)) {
    int current_gap = first_gap;
    while (current_gap > 0) {

        shellSort_pass (array, length, current_gap);

        if (current_gap == 1) {
            break;
        }
        current_gap = nextGap(current_gap);
    }
}

void shellSort_fixed (int* array, int length, int* gaps, int gaps_length) {
    int current_gap;

    for (int gap_ind = 0; gap_ind < gaps_length; gap_ind++){
        current_gap = gaps[gap_ind];
        shellSort_pass (array, length, current_gap);
    }
}

int ciura_gaps[] = {701, 301, 132, 57, 23, 10, 4, 1};


void shellSort_ciura (int* array, int length) {

    shellSort_fixed(array, length, ciura_gaps, 8);
}

void shellSort_knuth (int* array, int length) {

    int k = 1;
    int running_prod = 3;
    int current_gap = 1;
    while (current_gap < length / 3) {
        k++;
        running_prod *= 3;
        current_gap = (running_prod - 1) / 2;
    }
    
    int all_gaps[k];

    for (int i = k; i >= 1; i--) {
        all_gaps[k - i] = (running_prod - 1) / 2;
        running_prod /= 3;
    }

    shellSort_fixed(array, length, all_gaps, k);

}

int nextGap_random (int last_gap) {
    if (last_gap <= 4) {
        return 1;
    }
    else if (last_gap <= 10) {
        return 4;
    }
    else {
        int next_gap_h = (2 * last_gap) / 5;
        int next_gap_l = last_gap / 3;
        int next_gap = rand() % (next_gap_h - next_gap_l) + next_gap_l;
        if (!(next_gap % 2)) next_gap++;
        return next_gap;
    }
}


void shellSort_random (int* array, int length) {
    int first_gap = length;
    
    shellSort_dynamic(array, length, first_gap, nextGap_random);

}