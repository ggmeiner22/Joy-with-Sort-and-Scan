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

    def __le__(self, other):
        """Compare points based on their angle from the positive x-axis using acos."""
        norm_self = math.sqrt(self.x ** 2 + self.y ** 2)
        norm_other = math.sqrt(other.x ** 2 + other.y ** 2)
        angle_self = math.acos(self.x / norm_self) if norm_self != 0 else 0
        angle_other = math.acos(other.x / norm_other) if norm_other != 0 else 0
        return angle_self <= angle_other

def timsort(points):


def main():
    timsort_info = sys.argv[1]  # takes in the info file name

    data = sys.stdin.read().splitlines()
    num_of_points = int(data[0])
    # Creates a list of the points
    points = [Point(*map(float, line.split())) for line in data[1:num_of_points + 1]]

    timsort(points) #begin timsort

main()
