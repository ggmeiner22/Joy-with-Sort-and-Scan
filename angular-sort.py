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

    def compute_theta(self):
        x = self.get_x()
        y = self.get_y()

        vector_magnitude = math.sqrt(x ** 2 + y ** 2)
        if vector_magnitude == 0:
            raise ValueError("Cannot calculate theta for point at origin (0, 0)")

        cosine_theta  = x / vector_magnitude
        degree = math.acos(cosine_theta)

        # if in Quad 3 or 4
        if y < 0:
            degree = 2 * math.pi - degree

        return degree

    def __le__(self, other):
        return self.compute_theta() < other.compute_theta() or\
            self.compute_theta() == other.compute_theta()

    def __lt__(self, other):
        return self.compute_theta() < other.compute_theta()

    def __gt__(self, other):
        return self.compute_theta() > other.compute_theta()

    def __ge__(self, other):
        return self.compute_theta() > other.compute_theta() or\
            self.compute_theta() == other.compute_theta()

    def __eq__(self, other):
        return self.compute_theta() == other.compute_theta()


def timsort(points):
    """
    Performs TimSort on the given array of points.
    TimSort is a hybrid sorting algorithm derived from Merge Sort and Insertion Sort.
    It sorts small chunks using Insertion Sort and then merges them using a stack-based merging strategy.
    """
    stack = []
    total_runs = 0
    total_merges = 0
    arr_len = len(points)  # Length of points
    min_run = 3
    print("scanning phase:")

    index = 0
    while index < arr_len:


def insertion_sort(points, left, right):
    """Sorts a subarray using insertion sort"""
    print("before", points)
    for i in range(left + 1, right + 1):
        current_value = points[i]
        j = i - 1
        while j >= left and points[j] > current_value:
            points[j + 1] = points[j]
            j -= 1
        points[j + 1] = current_value
    print("after", points)


def main():
    timsort_info = sys.argv[1]  # takes in the info file name

    data = sys.stdin.read().splitlines()
    num_of_points = int(data[0])
    # Creates a list of the points
    points = [Point(*map(float, line.split())) for line in data[1:num_of_points + 1]]

    timsort(points)  # begin timsort


main()
