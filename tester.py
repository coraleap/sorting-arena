#!/usr/bin/env pypy
import ctypes

def list_to_clist (pyvals) -> ctypes.c_int:
    return (ctypes.c_int * len(pyvals))(*pyvals)

import os
os.chdir(os.path.dirname(__file__))

def fullpath(path) -> str:
    return os.path.abspath(os.path.join(os.getcwd(), path))

import numpy as np

import timeit


def pyth_writeConsInts(num: int) -> str:
    output = ''
    for i in range(1, num + 1):
        output = output + str(i) + ', '
    return output


# clibrary = ctypes.CDLL(fullpath("./compalgos/pdqsort.so"))

clibrary = ctypes.CDLL(fullpath("./compalgos/subtract.so"))

subtract = clibrary.subtract
subtract.argtypes = [ctypes.c_int, ctypes.c_int]
subtract.restype = ctypes.c_int

strincpy = clibrary.strincpy
strincpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
strincpy.restype = None

writeConsInts = clibrary.writeConsInts
writeConsInts.argtypes = [ctypes.c_int, ctypes.c_char_p]
writeConsInts.restype = ctypes.c_char_p

cheap = ctypes.CDLL(fullpath("./compalgos/heapsort.so"))
heap = cheap.array_sort
heap.argtypes = [ctypes.c_void_p, ctypes.c_int]
heap.restype = None

ctimsort = ctypes.CDLL(fullpath("./compalgos/timsort.so"))
timsorta = ctimsort.timsort
timsort = lambda a, b: timsorta(a, b, 4, ctimsort.comp)
timsort.argtypes = [ctypes.c_void_p, ctypes.c_int]
timsort.restype = None

from librarysort import librarySort

from shellsort import shellSort

from heapsort import heapSort as heap_py

from quicksort import quickSort_no_inds as quicksort

from patiencesort import patienceSort

class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('y', ctypes.c_int)]



def default_sort(arr: np.ndarray):
    return arr.sort()

def numpy_sort(arr: np.ndarray):
    return arr.sort(kind = 'heapsort')

def numpy_stablesort(arr: np.ndarray):
    return arr.sort(stable = True)

def init_arr(length: int, objtype: str = 'int', inptype: str = 'normal'):
    if inptype == 'normal':
        inp = np.arange(0, length)
        np.random.shuffle(inp)
        return inp
    if inptype == 'reversed':
        inp = np.arange(length - 1, -1, -1)
        return inp
    if inptype == 'sorted':
        return np.arange(0, length)
    
def verify_sorted(arr: list, target: list) -> bool:
    trues: iter = len(arr) == len(target) and list(arr[i] == target[i] for i in range(len(arr)))
    output: bool = all(trues)
    if not output:
        wrongind = trues.index(False)
        print(wrongind)
        print(arr[wrongind:])
    return output

def run_test(algo, length: int,
              objtype: str = 'int', inptype: str = 'normal', 
              lang : str = 'c') -> float:
    inp: np.ndarray = init_arr(length, objtype, inptype)
    target: np.ndarray = sorted(inp)
    if  lang.lower() == 'c':
        length = len(inp)
        inp: ctypes.c_void_p = list_to_clist(inp.tolist())
        timediff: float = time_func(algo, inp, length)
        inp: list = list(inp)

    elif lang.lower() == 'python':
        inp: list = inp.tolist()
        timediff: float = time_func(algo, inp)

    elif lang.lower() == 'numpy':
        timediff: float = time_func(algo, inp)
        inp: list = inp.tolist()
    
    if not verify_sorted(inp, target):
        raise Warning('Not Sorted!')
    return timediff
    
def run_tests(algo, length: int, num: int = 100, 
              objtype: str = 'int', inptype: str = 'normal', 
              lang : str = 'c', name : str | None = None, print_results: bool | None = True) -> np.ndarray:
    all_times: np.ndarray = np.zeros(num)
    num_warmup: int = int(num // 10 + 1)
    for i in range(num_warmup):
        run_test(algo, length, objtype, inptype, lang)
    for i in range(num):
        all_times[i] = run_test(algo, length, objtype, inptype, lang)
    if print_results:
        median: float = np.median(all_times)
        std_dev: float = np.std(all_times)
        print(f'{name:30} ... {median:8.4e} ... {std_dev:8.4e}')
    return all_times
    
def test_algos(algos: list[any], length: int, 
               num: int = 100, objtype: str = 'int', 
               inptype: str = 'normal') -> dict[str, np.ndarray]:
    output: dict = {}
    print(f'Test results, Array length = {length}, Number of trials = {num}')
    print(f'{"Name":30} ... {"Median":10} ... {"Standard Deviation":10}\n')
    for (name, algo) in algos.items():
        output[name] = run_tests(algo[0], length, num, objtype, inptype, algo[1], name, True)
    return output

def time_func(func, *args) -> float:
    t0: float = timeit.default_timer()
    func(*args)
    t1: float = timeit.default_timer()
    return t1 - t0

ALL_ALGOS: dict[str, tuple[any, str]] = {
    'Library Sort (Python)': (librarySort, 'python'),
    'Patience Sort (Python)': (patienceSort, 'python'),
    'Shell Sort (Python)': (shellSort, 'python'),
    'Heap Sort (Python)': (heap_py, 'python'),
    'Quick Sort (Python)': (quicksort, 'python'),
    'Tim Sort (C)': (timsort, 'c'),
    'Heap Sort (C)': (heap, 'c'),
    'Python Sort (Library)': (default_sort, 'python'),
    'Numpy Sort (Library)': (numpy_sort, 'numpy'),
    'Numpy Stable Sort (Library)': (numpy_stablesort, 'numpy')
}

def main() -> None:
    # a = ctypes.c_char_p(b"aab\0bccdd")
    # b = ctypes.c_char_p(b"      ")
    # c = 4
    # strincpy(b, a, c)

    # buf = ctypes.create_string_buffer(10 ** 5)
    # print(time_func(writeConsInts, 2 * 10 ** 4, buf))
    # print(time_func(pyth_writeConsInts, 2 * 10 ** 4))

    arrlen: int = 2 ** 16
    num: int = 1

    algos_ignored = {
        key: value for (key, value) in ALL_ALGOS.items()
        if key not in ['Quick Sort (Python)', 'Library Sort (Python)'] 
        # and key not in ['Shell Sort (Python)', 'Heap Sort (Python)']
    }

    test_algos(algos_ignored, arrlen, num, inptype = 'normal')

    # run_tests(heap, arrlen, name = 'Heap Sort')
    # run_tests(default_sort, arrlen, name = 'Python Sort', lang = 'python')
    # run_tests(numpy_sort, arrlen, name = 'Numpy Sort', lang = 'numpy')
    # run_tests(numpy_stablesort, arrlen, name = 'Numpy Stable Sort', lang = 'numpy')
    # print(f'Heap sort time: {run_test(heap, arrlen):8.3e}')
    # print(f'Standard sort time: {run_test(default_sort, arrlen, lang = 'python'):8.3e}')
    # print(f'Numpy sort time: {run_test(numpy_sort, arrlen, lang = 'numpy'):8.3e}')
    # print(f'Numpy stablesort time: {run_test(numpy_stablesort, arrlen, lang = 'numpy'):8.3e}')

if __name__ == '__main__':
    main()

