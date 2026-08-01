#==========================================================================================================================================#
#                                                       Algorithms
#==========================================================================================================================================#

# Linear Search and Binary Search
'''
NOTE Linear Search :
    Linear search starts at the beginning of a list and iterates through each item until it finds the target value it is looking for.

    If the target value is found, the index where it's located in the list is returned. If the target value isn't found, -1 is returned. 
    We return -1 because it's not a valid index in most programming languages.

    def linear_search(arr, target):
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1
    Time Complexity O(n) and Space Complexity is O(1) 

NOTE: Binary Search:
    Binary search works by dividing the list in half and checking if the target value is in the middle of the list. 
    If the target value is in the middle of the list, the index of the target value is returned. 
    Otherwise, the algorithm checks if the target value is in the left or right half of the list.

    def binary_search(arr, target):
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2  

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1
    Time Complexity O(log n) and Space Complexity is O(1) 
'''
# Divide and Conquer, and Merge Sort 
'''
NOTE Divide and Conquer Paradigm:
    The divide and conquer paradigm in computer science is a technique for recursively breaking down problems into smaller sub-problems.
    One of the key aspects of this technique is recursion, which happens when a function calls itself repeatedly until a base case is reached.


    def Merge_Sort(array: list) -> list:
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left = Merge_Sort(array[:mid])
        right = Merge_Sort(array[mid:])
        sorted_list = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])  
        return sorted_list 
    list1 = [13, 8, 5, 2]
    print(Merge_Sort(list1))

    Time Complexity is O(n log n) and Space Complexity O(n)
'''
