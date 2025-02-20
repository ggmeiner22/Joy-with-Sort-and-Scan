import sys
import math


class Point:

    def __init__(self, x, y):
        """
        Defines x and y variables
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """Defines how a point should print"""
        return "%s %s" % (self.x, self.y)

    def get_x(self):
        """
        :return: The x-coordinate of a point
        """
        return self.x

    def get_y(self):
        """
        :return: The y-coordinate of a point
        """
        return self.y

    def compute_degree(self):
        """
        Computes the angle (in radians) between the point and the x-axis.
        :return: Angle in radians
        """
        x = self.get_x()
        y = self.get_y()

        # Calculates the vector magnitude. Point is at the origin if 0.
        vector_magnitude = math.sqrt(x ** 2 + y ** 2)
        if vector_magnitude == 0:
            raise ValueError("Cannot calculate theta for point at origin (0, 0)")

        # Calculates the degree of the angle
        cosine_theta = x / vector_magnitude
        degree = math.acos(cosine_theta)

        # if in Quad 3 or 4
        if y < 0:
            degree = 2 * math.pi - degree

        return degree

    def __le__(self, other):
        """
        Defines the `<=` operator based on the computed degree.
        :param other: Another Point
        :return: True if this point's degree is less than or equal to the other's degree
        """
        return self.compute_degree() < other.compute_degree() or\
            self.compute_degree() == other.compute_degree()

    def __lt__(self, other):
        """
        Defines the `<` operator based on the computed degree.
        :param other: Another Point
        :return: True if this point's degree is less than the other's degree
        """
        return self.compute_degree() < other.compute_degree()

    def __gt__(self, other):
        """
        Defines the `>` operator based on the computed degree.
        :param other: Another Point
        :return: True if this point's degree is greater than the other's degree
        """
        return self.compute_degree() > other.compute_degree()

    def __ge__(self, other):
        """
        Defines the `>=` operator based on the computed degree.
        :param other: Another Point
        :return: True if this point's degree is greater than or equal to the other's degree
        """
        return self.compute_degree() > other.compute_degree() or\
            self.compute_degree() == other.compute_degree()

    def __eq__(self, other):
        """
        Defines the `==` operator based on the computed degree.
        :param other: Another Point
        :return: True if this point's degree is equal to the other's degree
        """
        return self.compute_degree() == other.compute_degree()


my_info_file = open(sys.argv[1], "w")


def timsort(points):
    """
    Performs TimSort on the given array of points.
    TimSort is a hybrid sorting algorithm derived from Merge Sort and Insertion Sort.
    It sorts small chunks using Insertion Sort and then merges them using a stack-based merging strategy.
    :param points: List of Point objects to be sorted
    """
    min_run = 32  # Minimum sub-array size for insertion sort
    runs = []  # Stack to manage merging runs
    total_runs = 0  # Counter for total runs found
    total_merges = 0  # Counter for total merges performed
    arr_len = len(points)  # Length of the array, points
    my_info_file.write("scanning phase:\n")

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
        my_info_file.write(f"run: [{start}, {end - start + 1}]\n")

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
                my_info_file.write(f"fixing invariant 1: merging runs [{z_start}, {z_len}] [{y_start}, {y_len}]\n")
                total_merges += 1  # Increment merge counter

                runs.append((z_start, z_len + y_len))  # Push the merged run back onto the stack
                runs.append(temp_item)  # Add x back to the stack
            elif y_len < x_len:
                runs.pop()  # Removes x
                runs.pop()  # Removes y
                merge(points, y_start, y_start + y_len - 1, x_start + x_len - 1)  # Merge runs

                my_info_file.write(f"fixing invariant 2: merging runs [{y_start}, {y_len}] [{x_start}, {x_len}]\n")
                total_merges += 1  # Increment merge counter
                runs.append((y_start, y_len + x_len))  # Push the merged run back onto the stack
            else:
                break  # Stop merging if the invariant holds

        # Move to the next potential run
        index = end + 1  # Set index to next unsorted element

    my_info_file.write("after scanning phase, stack contents are\n")
    for item in reversed(runs):  # prints stack contents in runs
        my_info_file.write(f"[{item[0]}, {item[1]}]\n")
    my_info_file.write("\nbottom-up merging phase:\n")  # Log start of bottom-up merging phase

    # Merge remaining runs while maintaining invariant
    temp_runs = []
    while len(runs) > 1:  # Continue until only one fully merged run remains
        top1_start, top1_len = runs.pop()  # Remove the topmost run
        top2_start, top2_len = runs.pop()  # Remove the second topmost run

        merge(points, top2_start, top2_start + top2_len - 1, top2_start + top2_len + top1_len - 1)  # Merge top two runs
        my_info_file.write(f"merging runs [{top2_start}, {top2_len}] [{top1_start}, {top1_len}]\n")  # Log merging
        total_merges += 1  # Increment merge counter
        temp_runs.append((top2_start, top2_len + top1_len))  # Push the merged run back onto the stack

        # Refill runs with the stack from temp_runs
        if len(runs) <= 1:
            while len(temp_runs) > 0:  # loops until stack is empty
                temp_start, temp_len = temp_runs.pop()
                runs.append((temp_start, temp_len))  # takes from top of temp_runs and puts back in runs

    # Log final statistics
    my_info_file.write(f"\ntotal number of runs found = {total_runs}\n")  # Log total runs detected
    my_info_file.write(f"total number of merges performed = {total_merges}\n")  # Log total merges performed
    return points


def merge(array, left_bound, middle, right_bound):
    """
    Merge two sorted sub-arrays into a single sorted sub-array.
    :param array: The original array containing sub-arrays to merge
    :param left_bound: Left index of the first sub-array
    :param middle: Middle index separating the two sub-arrays
    :param right_bound: Right index of the second sub-array
    """
    if middle == right_bound:
        return  # If the two sub-arrays are already merged, return immediately

    merged_list = []  # Temporary list to store merged elements
    left_pointer = left_bound  # Pointer for left sub-array
    right_pointer = middle + 1  # Pointer for right sub-array

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
    """
    Sorts a sub-array using insertion sort.
    :param points: List of Point objects
    :param left: Left index of the sub-array
    :param right: Right index of the sub-array
    """
    for index in range(left + 1, right + 1):
        current_value = points[index]
        j = index - 1
        while j >= left and points[j] > current_value:
            points[j + 1] = points[j]
            j -= 1
        points[j + 1] = current_value


def main():
    data = sys.stdin.read().splitlines()
    num_of_points = int(data[0])
    # Creates a list of the points
    points = [Point(*map(float, line.split())) for line in data[1:num_of_points + 1]]

    sorted_points = timsort(points)  # start timsort
    for point in sorted_points:
        x_val = point.get_x()
        y_val = point.get_y()
        # Formats in scientific notation if exponent is < -3
        if x_val != 0 and math.floor(math.log10(abs(x_val))) < -3:
            x_val = "{:.4E}".format(x_val).replace("E-0", "E-")
        if y_val != 0 and math.floor(math.log10(abs(y_val))) < -3:
            y_val = "{:.4E}".format(y_val).replace("E-0", "E-")
        print(f"{x_val} {y_val}")


main()
