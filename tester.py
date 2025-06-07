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

cquick = ctypes.CDLL(fullpath("./compalgos/quicksort.so"))
quick_LR = cquick.quickSort_LR
quick_LR.argtypes = [ctypes.c_void_p, ctypes.c_int]
quick_LR.restype = None

quick_LL = cquick.quickSort_LR
quick_LL.argtypes = [ctypes.c_void_p, ctypes.c_int]
quick_LL.restype = None

quick_LL_branchless = cquick.quickSort_LR
quick_LL_branchless.argtypes = [ctypes.c_void_p, ctypes.c_int]
quick_LL_branchless.restype = None

introsort_one = cquick.intro_sort_onemedian
introsort_one.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
introsort_one.restype = None

introsort_three = cquick.intro_sort_threemedian
introsort_three.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
introsort_three.restype = None

quick_median_finder = cquick.quick_MoMpivot
quick_median_finder.argtypes = [ctypes.c_void_p, ctypes.c_int]
quick_median_finder.restype = None


cshell = ctypes.CDLL(fullpath("./compalgos/shellsort.so"))
shell_ciura = cshell.shellSort_ciura
heap.argtypes = [ctypes.c_void_p, ctypes.c_int]
heap.restype = None

shell_random = cshell.shellSort_random
heap.argtypes = [ctypes.c_void_p, ctypes.c_int]
heap.restype = None

shell_knuth = cshell.shellSort_knuth
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
    return arr.sort()

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

def format_str(inp, maxlen):
    if len(inp) > maxlen:
        inp = inp[:maxlen]
    return ' '.join([word[0].upper() + word[1:] for word in inp.split(' ')])

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
              objtype: str = 'int', inptype: str = 'normal', name : str | None = None, print_results: bool | None = True) -> np.ndarray:
    all_times: np.ndarray = np.zeros(num)
    num_warmup: int = int(num // 10 + 1)
    for i in range(num_warmup):
        run_test(algo['algo'], length, objtype, inptype, algo['type_internal'])
    for i in range(num):
        all_times[i] = run_test(algo['algo'], length, objtype, inptype, algo['type_internal'])
    if print_results:
        mean: float = np.mean(all_times)
        std_dev: float = np.std(all_times)
        print(f'{name:36} ... {format_str(algo['type_external'], 10):10} ... {algo['average_case_tc']:20} ... {mean:6.2e} ... {std_dev:6.2e}')
    return all_times
    
def test_algos(algos: list[any], length: int, 
               num: int = 100, objtype: str = 'int', 
               inptype: str = 'normal') -> dict[str, np.ndarray]:
    output: dict = {}
    print(f'Test results, Array length = {length}, Number of trials = {num}')
    print(f'{"Name":36} ... {"Language":10} ... {"Avg. Time Complexity":20} ... {"Mean":8} ... {"Standard Deviation":8}\n')
    for (name, algo) in algos.items():
        output[name] = run_tests(algo, length, num, objtype, 'normal', name, True)
    return output

def time_func(func, *args) -> float:
    t0: float = timeit.default_timer()
    func(*args)
    t1: float = timeit.default_timer()
    return t1 - t0


    

all_algos: dict[str, tuple[any, str]] = {
    'Library Sort': {
        'algo': librarySort,
        'type_internal': 'python',
        'type_external': 'python',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(n)',
        'stable': False,
    },
    'Patience Sort': {
        'algo': patienceSort,
        'type_internal': 'python',
        'type_external': 'python',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(n)',
        'stable': False
    },
    'Shell Sort': {
        'algo': shellSort,
        'type_internal': 'python',
        'type_external': 'python',
        'worst_case_tc': 'Unknown',
        'average_case_tc': 'Unknown',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Heap Sort (Python)': {
        'algo': heap_py,
        'type_internal': 'python',
        'type_external': 'python',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Quick Sort (Vanilla, Python)': {
        'algo': quicksort,
        'type_internal': 'python',
        'type_external': 'python',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Tim Sort': {
        'algo': timsort,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(n)',
        'stable': True
    },
    'Heap Sort (C)': {
        'algo': heap,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Quick Sort - LR Ptrs': {
        'algo': quick_LR,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Quick Sort - LL Ptrs': {
        'algo': quick_LL,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Quick Sort - LL Ptrs, Branchless': {
        'algo': quick_LL_branchless,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Quick Sort - Median Find Pvt': {
        'algo': quick_median_finder,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Shell Sort - Ciura Gaps': {
        'algo': shell_ciura,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n^2)',
        'average_case_tc': 'O(n^2)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Shell Sort - Random Gaps (C)': {
        'algo': shell_random,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n^2)*',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Shell Sort - Knuth Gaps (C)': {
        'algo': shell_knuth,
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'Unknown',
        'average_case_tc': 'Unknown',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Python sort()': {
        'algo': default_sort,
        'type_internal': 'python',
        'type_external': 'std. lib',
        'worst_case_tc': 'Unknown',
        'average_case_tc': 'Unknown',
        'space_complexity': 'O(n)',
        'stable': True
    },
    'Numpy sort()': {
        'algo': numpy_sort,
        'type_internal': 'numpy',
        'type_external': 'std. lib',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(1)',
        'stable': False
    },
    'Numpy sort() stable': {
        'algo': numpy_stablesort,
        'type_internal': 'numpy',
        'type_external': 'std. lib',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(n)',
        'stable': True
    },
}

all_algos.update({
    f'IntroSort - Lazy Pvt, Minlen {n}': {
        'algo': lambda arr, l: introsort_one(arr, l, n),
        'type_internal': 'c',
        'type_external': 'c',
        'worst_case_tc': 'O(n log n)',
        'average_case_tc': 'O(n log n)',
        'space_complexity': 'O(n)',
        'stable': True
    } for n in np.logspace(4, 7, num = 4, base = 2, dtype = int)
    })

all_algos.update({
    f'IntroSort - 3-Median, Minlen {n}': {
    'algo': lambda arr, l: introsort_three(arr, l, n),
    'type_internal': 'c',
    'type_external': 'c',
    'worst_case_tc': 'O(n log n)',
    'average_case_tc': 'O(n log n)',
    'space_complexity': 'O(n)',
    'stable': True
    } for n in np.logspace(4, 7, num = 4, base = 2, dtype = int)
})


LIBRARY_SORTS: dict[str, tuple[any, str]] = {
    key: value for (key, value) in all_algos.items() if value['type_external'] == 'std. lib' 

}

C_SORTS: dict[str, tuple[any, str]] = {
    key: value for (key, value) in all_algos.items() if value['type_external'] == 'c' 
}

PY_SORTS: dict[str, tuple[any, str]] = {
    key: value for (key, value) in all_algos.items() if value['type_external'] == 'python' 
}

VULNERABLE_SORTS: dict[str, tuple[any, str]] = {
    key: value for (key, value) in all_algos.items() if value['worst_case_tc'] == 'O(n^2)'
}

def main() -> None:
    # a = ctypes.c_char_p(b"aab\0bccdd")
    # b = ctypes.c_char_p(b"      ")
    # c = 4
    # strincpy(b, a, c)

    # buf = ctypes.create_string_buffer(10 ** 5)
    # print(time_func(writeConsInts, 2 * 10 ** 4, buf))
    # print(time_func(pyth_writeConsInts, 2 * 10 ** 4))

    arrlen: int = 2**15
    num: int = 100

    algos_no_py = dict(C_SORTS, **LIBRARY_SORTS)
    # selected_algos = algos_no_py
    selected_algos = all_algos

    algos_ignored = {
        key: value for (key, value) in selected_algos.items()
        # if key not in VULNERABLE_SORTS
        # if key not in ['Quick Sort (Python)', 'Library Sort (Python)'] 
        # and key not in ['Shell Sort (Python)', 'Heap Sort (Python)']
    }

    algos_in_order = {}

    algos_in_order.update(PY_SORTS)
    algos_in_order.update(C_SORTS)
    algos_in_order.update(LIBRARY_SORTS)


    test_algos(algos_in_order, arrlen, num, inptype = 'normal')
    # test_algos({
    #     key: value for (key, value) in selected_algos.items() if key[:13] == 'Introspective'
    # }, arrlen, num, inptype = 'normal')

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

