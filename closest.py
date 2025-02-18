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

    def compute_distance(self):
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
        return self.compute_distance() < other.compute_distance() or\
            self.compute_distance() == other.compute_distance()

    def __lt__(self, other):
        return self.compute_distance() < other.compute_distance()

    def __gt__(self, other):
        return self.compute_distance() > other.compute_distance()

    def __ge__(self, other):
        return self.compute_distance() > other.compute_distance() or\
            self.compute_distance() == other.compute_distance()

    def __eq__(self, other):
        return self.compute_distance() == other.compute_distance()


def main():
    data = sys.stdin.read().splitlines()
    # Creates a list of the points
    points = [Point(*map(float, line.split())) for line in data]
    print(points)


main()
