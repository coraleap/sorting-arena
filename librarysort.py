#!/usr/bin/env pypy

def binSearch(arr: list, low: int, high: int, x: any) -> int:
    
    if high - low <= 1:
        return high
    
    mid: int = (high + low) // 2
    try:
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binSearch(arr, low, mid, x)
        else:
            return binSearch(arr, mid, high, x)
    except IndexError as e:
        print(arr)
        print(low)
        print(high)
        raise e

def findNext(arr: list, ind: int) -> int:
    curr: int = ind    
    arrlen: int = len(arr)
    while (curr < arrlen and (arr[curr] is not None)):
        curr += 1
    if curr == arrlen:
        arr.append(None)
    return curr

def insertTo(arr: list, x: any, highguess: int) -> None:
    curr: int = highguess
    arrlen: int = len(arr)

    while curr > 0 and (arr[curr] is None or arr[curr] > x):
        curr -= 1
    insertInd: int = findNext(arr, curr)
    arr[insertInd] = x

def redouble(arr: list, gapSize: int) -> list:
    arrlen: int = len(arr)

    output = [None for _ in range(arrlen * gapSize)]
    for i in range(arrlen):
        output[i * gapSize] = arr[i]
    
    return output


def insertionSort(arr: list) -> None:
    for sortedLength in range(1, len(arr)):
        nextElement: any = arr[sortedLength]
        nextInd: int = sortedLength
        while nextInd > 0 and nextElement < arr[nextInd - 1]:
            arr[nextInd] = arr[nextInd - 1]
            nextInd -= 1
        arr[nextInd] = nextElement

def removeGaps(arr: list) -> list:
    return [x for x in arr if x is not None]

MIN_LIB = 64

def librarySort(arr: list, gapSize: int = 3, redoubleSize: float = 2) -> None:
    if len(arr) < MIN_LIB:
        insertionSort(arr)
        return None
    libSizes: list[int] = [len(arr)]
    while (libSizes[-1] >= MIN_LIB):
        libSizes.append(int(libSizes[-1] // redoubleSize))
    libSizes.reverse()

    currentLib: list = arr[:libSizes[0]]
    insertionSort(currentLib)


    for lastSize, currentSize in zip(libSizes, libSizes[1:]): 
        wideLib: list = redouble(currentLib, gapSize)
        for i in range(lastSize, currentSize):
            x: any = arr[i]
            highguess: int = binSearch(currentLib, 0, lastSize, x) * gapSize - 1
            insertTo(wideLib, x, highguess)
        wideLib = removeGaps(wideLib)
        insertionSort(wideLib)
        currentLib = wideLib
    for i in range(len(arr)):
        arr[i] = currentLib[i]


    

def main():
    arr1 = [int(((42747 * i ** 3.5 + 1014 * i ** 1.5 + 12479) % 781) // 1) for i in range(200000)]
    librarySort(arr1)
    # print(arr1)

if __name__ == "__main__":
    main()
    