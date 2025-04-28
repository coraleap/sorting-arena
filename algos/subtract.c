/*

*/
#include <string.h>
#include <stdio.h>

int subtract (int a, int b) {
    return a - b;
}

void strincpy (char* writestr, char* readstr, int length) {
    strncpy(writestr, readstr, length);
}

char *allocate_memory (int amount) {
    return calloc()
}

void *writeConsInts (int num, char* outptr) {
    int maxDigits = 0;
    int numQuot = num;
    while (numQuot) {
        numQuot /= 10;
        maxDigits++;
    }

    char* output = outptr;
    char* writer = outptr;

    char bufferstr[maxDigits + 2];
    char* buffer = bufferstr;

    for (int i = 1; i <= num; i++) {
        sprintf(buffer, "%d, ", i);
        strncat(writer, buffer, maxDigits + 2);
        writer += strlen(buffer);
    }

    *(writer) = 0;

    return output;
}

int main() {
    char out[10000];
    writeConsInts(100, out);
    printf("\n%s", out);
}