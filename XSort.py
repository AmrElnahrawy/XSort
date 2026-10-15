import random

class XSort:
    @staticmethod
    def make_array(size, shuffling_style, seed=None):
        arr = list(range(1, size + 1))
        if shuffling_style == "Decreasing":
            arr.reverse()
        elif shuffling_style == "Randomized":
            random.Random(seed).shuffle(arr)
        return arr

    @staticmethod
    def selection_sort(arr: list):
        for i in range(0, len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                yield i, j, min_idx
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield i, min_idx

    @staticmethod
    def insertion_sort(arr: list):
        for i in range(1, len(arr)):
            j = i
            while j > 0:
                yield j - 1, j
                if arr[j] >= arr[j - 1]:
                    break
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1

    @staticmethod
    def bubble_sort(arr: list):
        for i in range(0, len(arr)):
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield j, j + 1

    ALGORITHMS = {
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Bubble Sort": bubble_sort,
    }