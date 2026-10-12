#Bubblesort

import matplotlib.pyplot as plt
import random

def bubble_sort(arr):

    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

# For comparison - quicksort

def quicksort(arr):

    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

# Performance graph

sizes = [100, 200, 400, 800, 1600]

bubble_times = []

quick_times = []

for size in sizes:

    data = [random.randint(0, size) for _ in range(size)]
    # Bubble Sort timing
    arr = data.copy()
    start = time.time()
    bubble_sort(arr)
    bubble_times.append(time.time() - start)
    # Quicksort timing
    arr = data.copy()
    start = time.time()
    quicksort(arr)
    quick_times.append(time.time() - start)

plt.plot(sizes, bubble_times, label='Bubble Sort')

plt.plot(sizes, quick_times, label='Quicksort')

plt.xlabel('Input Size (n)')

plt.ylabel('Time (seconds)')

plt.title('Bubble Sort vs Quicksort Performance')

plt.legend()

plt.show()

 Time Complexity Analysis
 
	Bubble Sort: 
	Best case: O(n)(already sorted)
	Average/Worst case: O(n^2 )
	Quicksort: 
	Best/Average case: O(n log⁡n )
	Worst case: O(n^2 )(rare, with poor pivot choice)

Report 

Bubble sort is a simple comparison-based sorting algorithm. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. This process is repeated until the list is sorted. Due to its straightforward structure, bubble sort is easy to implement and understand, making it suitable for educational purposes.

In terms of efficiency, bubble sort performs adequately on very small datasets and nearly sorted data, as its best-case time complexity is O(n). However, for average and worst-case scenarios—particularly with larger or randomly ordered datasets—its time complexity is O(n^2 ). This quadratic growth means that bubble sort becomes impractically slow as the dataset size increases.

In contrast, quicksort is a more sophisticated divide-and-conquer algorithm. By partitioning the array around a pivot, it recursively sorts the subarrays, achieving an average-case time complexity of O(n log⁡n ). This makes quicksort dramatically faster than bubble sort for large datasets and is why quicksort is often used in real-world applications.

The accompanying graph illustrates how bubble sort’s runtime increases much more rapidly than quicksort’s as input size grows. For small arrays (e.g., n<200), the difference is negligible, but as it increases, quicksort’s superior efficiency becomes clear.

In practice, bubble sort is mainly used for teaching fundamental sorting concepts or for trivial cases with tiny data. Quicksort, however, is broadly used in production systems due to its speed and efficiency, especially for large or unsorted datasets.


