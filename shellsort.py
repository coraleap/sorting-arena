#!/usr/bin/env pypy
"""
Basic shellsort implementation taken from Wikipedia: https://en.wikipedia.org/wiki/Shellsort

Used for benchmarking of Python programs
"""

def shellSort(a: list) -> None:
    n: int = len(a)


    gaps: list[int] = []  # Sedgewick
    nextgap = 1

    while (nextgap < n):
        gaps.append(nextgap)
        k: int = len(gaps) 
        nextgap = 4 ** k + 3 * 2 ** (k - 1) + 1

    gaps.reverse()
    # Start with the largest gap and work down to a gap of 1
    # similar to insertion sort but instead of 1, gap is being used in each step
    for gap in gaps:
        # Do a gapped insertion sort for every element in gaps
        # Each loop leaves a[0..gap-1] in gapped order
        for i in range(gap, n):
            # save a[i] in temp and make a hole at position i
            temp = a[i]
            # shift earlier gap-sorted elements up until the correct location for a[i] is found
            j: int = i
            while (j >= gap and a[j - gap] > temp):
                a[j] = a[j - gap]
                j -= gap
            # put temp (the original a[i]) in its correct location
            a[j] = temp


def main():
    arr1 = [int(((42747 * i ** 3.5 + 1014 * i ** 1.5 + 12479) % 781) // 1) for i in range(200)]
    shellSort(arr1)
    print(arr1)

if __name__ == "__main__":
    main()