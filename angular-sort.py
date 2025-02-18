import sys
import math


class Point:

    def __init__(self, x, y):
        """Defines x and y variables"""
        self.x = x
        self.y = y

    def __repr__(self):
        """Defines how a point should print"""
        return "%s %s" % (self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def compute_degree(self):
        x = self.get_x()
        y = self.get_y()

        vector_magnitude = math.sqrt(x ** 2 + y ** 2)
        if vector_magnitude == 0:
            raise ValueError("Cannot calculate theta for point at origin (0, 0)")

        cosine_theta = x / vector_magnitude
        degree = math.acos(cosine_theta)

        # if in Quad 3 or 4
        if y < 0:
            degree = 2 * math.pi - degree

        return degree

    def __le__(self, other):
        return self.compute_degree() < other.compute_degree() or\
            self.compute_degree() == other.compute_degree()

    def __lt__(self, other):
        return self.compute_degree() < other.compute_degree()

    def __gt__(self, other):
        return self.compute_degree() > other.compute_degree()

    def __ge__(self, other):
        return self.compute_degree() > other.compute_degree() or\
            self.compute_degree() == other.compute_degree()

    def __eq__(self, other):
        return self.compute_degree() == other.compute_degree()


def timsort(points):
    """
    Performs TimSort on the given array of points.
    TimSort is a hybrid sorting algorithm derived from Merge Sort and Insertion Sort.
    It sorts small chunks using Insertion Sort and then merges them using a stack-based merging strategy.
    """
    min_run = 32  # Minimum subarray size for insertion sort
    runs = []  # Stack to manage merging runs
    total_runs = 0  # Counter for total runs found
    total_merges = 0  # Counter for total merges performed
    arr_len = len(points)  # Length of the array, points
    print("scanning phase:")

    index = 0  # Initialize index for scanning the array
    while index < arr_len:
        start = index  # Mark the starting index of a run
        end = min(index + min_run, arr_len) - 1  # Determine the minimum endpoint of the run

        # Sort this small section using insertion sort
        insertion_sort(points, start, end)

        # Extend the run if adjacent elements continue increasing
        while end + 1 < arr_len and points[end] <= points[end + 1]:
            end += 1

        # Store the run's start index and size in the list
        runs.append((start, end - start + 1))
        total_runs += 1  # Increment the run counter
        index = end + 1  # Move to the next potential run
        print(f"run: [{start}, {end - start + 1}]")

        # Check and maintain the TimSort merging invariant
        # Check and maintain the TimSort merging invariant
        while len(runs) >= 3:  # Ensure there are at least 3 runs for merging
            x_start, x_len = runs[-1]  # Retrieve the most recent run
            y_start, y_len = runs[-2]  # Retrieve the second most recent run
            z_start, z_len = runs[-3]  # Retrieve the third most recent run

            if z_len < x_len + y_len:  # Check if the merging invariant is violated
                temp_item = runs.pop()  # Removes x
                runs.pop()  # Remove y
                runs.pop()  # Removes z

                merge(points, z_start, z_start + z_len - 1, y_start + y_len - 1)  # Merge runs
                print(f"fixing invariant 1: merging runs [{z_start}, {z_len}] [{y_start}, {y_len}]")  # Log merging
                total_merges += 1  # Increment merge counter

                runs.append((z_start, z_len + y_len))  # Push the merged run back onto the stack
                runs.append(temp_item)  # Add x back to the stack
            elif y_len < x_len:
                runs.pop()  # Removes x
                runs.pop()  # Removes y
                merge(points, y_start, y_start + y_len - 1, x_start + x_len - 1)  # Merge runs

                print(f"fixing invariant 2: merging runs [{y_start}, {y_len}] [{x_start}, {x_len}]")  # Log merging
                total_merges += 1  # Increment merge counter
                runs.append((y_start, y_len + x_len))  # Push the merged run back onto the stack
            else:
                break  # Stop merging if the invariant holds

        # Move to the next potential run
        index = end + 1  # Set index to next unsorted element

    print("after scanning phase, stack contents are")
    for item in reversed(runs):  # prints stack contents in runs
        print(f"[{item[0]}, {item[1]}]")
    print("\nbottom-up merging phase:")  # Log start of bottom-up merging phase

    # Merge remaining runs while maintaining invariant
    temp_runs = []
    while len(runs) > 1:  # Continue until only one fully merged run remains
        top1_start, top1_len = runs.pop()  # Remove the topmost run
        top2_start, top2_len = runs.pop()  # Remove the second topmost run

        merge(points, top2_start, top2_start + top2_len - 1, top2_start + top2_len + top1_len - 1)  # Merge top two runs
        print(f"merging runs [{top2_start}, {top2_len}] [{top1_start}, {top1_len}]")  # Log merging
        total_merges += 1  # Increment merge counter
        temp_runs.append((top2_start, top2_len + top1_len))  # Push the merged run back onto the stack

        # Refill runs with the stack from temp_runs
        if len(runs) <= 1:
            while len(temp_runs) > 0:  # loops until stack is empty
                temp_start, temp_len = temp_runs.pop()
                runs.append((temp_start, temp_len))  # takes from top of temp_runs and puts back in runs

    # Log final statistics
    print(f"\ntotal number of runs found = {total_runs}")  # Log total runs detected
    print(f"total number of merges performed = {total_merges}")  # Log total merges performed


def merge(array, left_bound, middle, right_bound):
    """
    Merge two sorted sub-arrays into a single sorted subarray.
    The left subarray is array[left_bound:middle+1] and the right subarray is array[middle+1:right_bound+1].
    """
    if middle == right_bound:
        return  # If the two sub-arrays are already merged, return immediately

    merged_list = []  # Temporary list to store merged elements
    left_pointer = left_bound  # Pointer for left subarray
    right_pointer = middle + 1  # Pointer for right subarray

    # Merge the two sorted sub-arrays by comparing elements
    while left_pointer <= middle and right_pointer <= right_bound:
        if array[left_pointer] <= array[right_pointer]:  # If left element is smaller, add it
            merged_list.append(array[left_pointer])
            left_pointer += 1
        else:  # If right element is smaller, add it
            merged_list.append(array[right_pointer])
            right_pointer += 1

    # Append remaining elements from the left sub-array (if any)
    while left_pointer <= middle:
        merged_list.append(array[left_pointer])
        left_pointer += 1

    # Append remaining elements from the right sub-array (if any)
    while right_pointer <= right_bound:
        merged_list.append(array[right_pointer])
        right_pointer += 1

    # Copy merged elements back into the original array at the correct positions
    for index, sorted_value in enumerate(merged_list):
        array[left_bound + index] = sorted_value  # Overwrite original array with sorted elements


def insertion_sort(points, left, right):
    """Sorts a subarray using insertion sort"""
    for index in range(left + 1, right + 1):
        current_value = points[index]
        j = index - 1
        while j >= left and points[j] > current_value:
            points[j + 1] = points[j]
            j -= 1
        points[j + 1] = current_value


def main():
    # timsort_info = sys.argv[1]  # takes in the info file name

    data = sys.stdin.read().splitlines()
    num_of_points = int(data[0])
    # Creates a list of the points
    points = [Point(*map(float, line.split())) for line in data[1:num_of_points + 1]]

    timsort(points)  # start timsort


main()
