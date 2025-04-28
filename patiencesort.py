def binSearch(arr: list, low: int, high: int, x: any) -> int:
    if high - low <= 1:
        if low == high:
            return low
        if arr[low] <= x:
            return high
        else:
            return low
    
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

def siftDown(arr: list[list[any, int]], n, i):
    smallest = i  # Initialize largest as root
    l = 2 * i + 1  # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

 # See if left child of root exists and is
 # greater than root
    if l < n and arr[i][1] > arr[l][1]:
        smallest = l

 # See if right child of root exists and is
 # greater than root

    if r < n and arr[smallest][1] > arr[r][1]:
        smallest = r

 # Change root, if needed
    if smallest != i:
        (arr[i], arr[smallest]) = (arr[smallest], arr[i])  # swap

        # Sift down on the root.
        siftDown(arr, n, smallest)

def create_piles(arr: list) -> tuple[list[list], list]:
    piles: list[list] = []
    fronts: list = []
    for a in arr:
        pileInd = binSearch(fronts, 0, len(fronts), a)
        if pileInd == len(fronts):
            fronts.append(a)
            piles.append([a])
        else:
            fronts[pileInd] = a
            piles[pileInd].append(a)
    return (piles, fronts)

def combine_piles(arr: list, piles: list[list], fronts: list) -> list:
    formerfronts: list = fronts
    fronts: list[list[int, any]] = []
    for i, val in enumerate(formerfronts):
        fronts.append([i, val])
    
    for i in range(len(arr)):
        arr[i] = fronts[0][1]
        pile = piles[fronts[0][0]]
        pile.pop()

        if not pile:
            (fronts[0], fronts[-1]) = (fronts[-1], fronts[0])
            fronts.pop()
        else:
            fronts[0][1] = pile[-1]
        
        siftDown(fronts, len(fronts), 0)

def patienceSort(arr: list) -> None:
    (piles, fronts) = create_piles(arr)
    combine_piles(arr, piles, fronts)


    

def main() -> None:
    arr: list[int] = [1, 5, 2, 1, 5, 2, 4, 1]
    patienceSort(arr)
    print(arr)


if __name__ == "__main__":
    main()