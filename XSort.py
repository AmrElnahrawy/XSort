import time
class XSort:
    @staticmethod
    def selection_sort(arr: list, delay_time: int) -> list:
        for i in range(0, len(arr)):
            min_value = arr[i]
            for j in range(i + 1, len(arr)):
                time.sleep(delay_time)
                min_value = min(min_value, arr[j])

        return arr

    @staticmethod
    def insertion_sort(arr: list, delay_time: int) -> list:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                time.sleep(delay_time)
                arr[j + 1], arr[j] = arr[j], arr[j + 1]
                j -= 1

        return arr

    @staticmethod
    def bubble_sort(arr: list, delay_time: int) -> list:
        for i in range(0, len(arr)):
            for j in range(0, len(arr) - i - 1):
                time.sleep(delay_time)
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr
