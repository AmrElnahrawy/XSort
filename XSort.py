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
                yield j,
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    @staticmethod
    def insertion_sort(arr: list):
        for i in range(1, len(arr)):
            j = i
            while j > 0:
                if arr[j] >= arr[j - 1]:
                    break
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                yield j - 1,
                j -= 1

    @staticmethod
    def bubble_sort(arr: list):
        for i in range(0, len(arr)):
            is_sorted = True
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    is_sorted = False
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield j + 1,
            if is_sorted:
                break

    @staticmethod
    def __merge(arr: list, left: int, mid: int, right: int):
        i = j = 0
        k = left
        left_arr = arr[left:mid]
        right_arr = arr[mid:right]

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                yield k, left + i
                i += 1
            else:
                arr[k] = right_arr[j]
                yield k, mid + j
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            yield k, left + i
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            yield k, mid + j
            j += 1
            k += 1

    @staticmethod
    def merge_sort_recursive(arr: list, left = 0, right = None):
        if right is None:
            right = len(arr)
        if right - left <= 1:
            return
        middle = left + (right - left) // 2
        yield from XSort.merge_sort_recursive(arr, left, middle)
        yield from XSort.merge_sort_recursive(arr, middle, right)
        yield from XSort.__merge(arr, left, middle, right)


    @staticmethod
    def merge_sort_iterative(arr: list):
        current_size = 1
        while current_size < len(arr):
            left = 0
            while left < len(arr) - 1:
                middle = min(left + current_size, len(arr))
                right = min(left + 2 * current_size, len(arr))
                yield from XSort.__merge(arr, left, middle, right)
                left += 2 * current_size
            current_size *= 2

    def quick_sort(arr: list):
        pass

    def heap_sort(arr: list):
        pass

    def radix_sort(arr: list):
        pass



    ALGORITHMS = {
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Bubble Sort": bubble_sort,
        "Merge Sort (Recursive)": merge_sort_recursive,
        "Merge Sort (Iterative)": merge_sort_iterative,
        "Quick Sort": quick_sort,
    }