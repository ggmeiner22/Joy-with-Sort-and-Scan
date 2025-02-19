import sys
import math
from functools import cmp_to_key


class Point:
    def __init__(self, x, y):
        """
        Initializes a Point with x and y coordinates.
        :param x: x-coordinate of the point.
        :param y: y-coordinate of the point.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        """
        Returns a string representation of the Point.
        """
        return "%s %s" % (self.x, self.y)

    def get_x(self):
        """
        Returns the x-coordinate of the point.
        """
        return self.x

    def get_y(self):
        """
        Returns the y-coordinate of the point.
        """
        return self.y

    def distance(self, other):
        """
        Computes the Euclidean distance between two points.
        :param other: Second Point object.
        :return: Euclidean distance between current Point and another point.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __lt__(self, other):
        """
        Overloads the < operator to compare points based on y-coordinates.
        :param other: Another Point object.
        :return: True if this point's y-coordinate is less than the other's.
        """
        return self.y < other.y

    def __le__(self, other):
        """
        Overloads the <= operator to compare points based on y-coordinates.
        :param other: Another Point object.
        :return: True if this point's y-coordinate is less than or equal to the other's.
        """
        return self.y <= other.y

    def __eq__(self, other):
        """
        Overloads the == operator for comparing y-coordinates using floating-point tolerance.
        :param other: Another Point object.
        :return: True if y-coordinates are approximately equal.
        """
        return math.isclose(self.y, other.y, rel_tol=1e-8)


def compare_x_value(left_value, right_value):
    """
    Comparator function for sorting by x-coordinate
    :param left_value: First Point object.
    :param right_value: Second Point object.
    :return: -1 if left_value.x < right_value.x, 1 if greater, 0 if equal.
    """
    if left_value.x < right_value.x:
        return -1
    elif left_value.x > right_value.x:
        return 1
    else:
        return 0


def closest_distance_sweep_line(points):
    """
    Finds the closest distance between a pair of points using a sweep line algorithm.
    :param points: List of Point objects.
    :return: The shortest distance found between any two points.
    """
    points_len = len(points)
    if points_len < 2:
        return float('inf')

    # Use a binary search tree to hold points sorted by y
    bst = BST()
    bst.insert(points[0])

    # Initialize the closest pair distance
    D = float('inf')

    pi = 0  # Left boundary index

    for j in range(1, points_len):
        pj = points[j]  # Initialize right boundary index point

        # Remove points outside the current D x 2D window
        while pi < j and pj.x - points[pi].x > D:
            bst.remove(points[pi].y)
            pi += 1

        # Query the binary search tree for points within the D x 2D bounding box
        successor = bst.successor(pj.y)
        predecessor = bst.predecessor(pj.y)

        # Check valid nearby points
        candidates = []
        if successor:
            candidates.append(successor.value)
        if predecessor:
            candidates.append(predecessor.value)

        # Check the distance of each valid group of points
        # save the smallest in D if smaller than current D value
        for pk in candidates:
            distance = pj.distance(pk)
            if distance < D:
                D = distance

        # Insert current point into the binary search tree
        bst.insert(pj)

    return D


class TreeNode:
    def __init__(self, value):
        """
        Creates a new TreeNode object for the binary search tree.
        :param value: The value to be stored in the node (Point object).
        """
        self.value = value  # Stores the Point object or other data
        self.left = None
        self.right = None
        self.parent = None


class BST:
    def __init__(self):
        """
        Creates a new, empty binary search tree object
        """
        self.root = None

    def insert(self, value):
        """
        Insert a node with value as the Point object
        :param value: The Point object to insert.
        """
        new_node = TreeNode(value)
        if not self.root:
            self.root = new_node
            return

        current = self.root
        while True:
            if value < current.value:
                if current.left:
                    current = current.left
                else:
                    current.left = new_node
                    new_node.parent = current
                    break
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = new_node
                    new_node.parent = current
                    break

    def remove(self, value):
        """
        Removes a node from the binary search tree based on its y-coordinate value.
        :param value: y-coordinate of the point to remove.
        """
        current = self.root  # Start at the root node
        parent = None  # Pointer to track the parent node

        # # Find the node to be removed by traversing the binary search tree
        while current and current.value.y != value:
            parent = current
            if value < current.value.y:
                current = current.left  # Move left if the value is smaller
            else:
                current = current.right  # Move left if the value is larger

        # If no node is found with the given value, return
        if not current:
            return

        # If the node is a leaf node (has no children)
        if not current.left and not current.right:
            if not parent:
                self.root = None  # If the tree had only one node, it becomes empt
            elif parent.left == current:
                parent.left = None  # Remove the reference from the parent
            else:
                parent.right = None  # Remove the reference from the parent

        # If the node has one child
        elif not current.left or not current.right:
            child = current.left if current.left else current.right  # Find the existing child
            if not parent:
                self.root = child  # Update root if removing root node
            elif parent.left == current:
                parent.left = child  # Update parent's left child
            else:
                parent.right = child  # Update parent's right child

        # If the node has two children
        else:
            successor_parent = current
            successor = current.right
            while successor.left:  # Find inorder successor
                successor_parent = successor
                successor = successor.left

            current.value = successor.value  # Copy successor value to current node

            # Remove successor node
            if successor_parent.left == successor:
                successor_parent.left = successor.right  # Update parent's left reference
            else:
                successor_parent.right = successor.right  # Update parent's right reference

    def find(self, value):
        """
        Finds and returns the node containing value, or None if not found
        :param value: The Point object to insert.
        :return: returns the value if found, otherwise returns None
        """
        current = self.root
        while current:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None

    def successor(self, value, strict=False):
        """
        Finds the smallest node greater than or equal to value.
        :param value: y-coordinate value to find successor for.
        :param strict: If True, finds strictly greater value.
        :return: Successor TreeNode or None.
        """
        result = None
        current = self.root
        while current:
            if current.value.y > value or (not strict and current.value.y == value):
                result = current
                current = current.left
            else:
                current = current.right
        return result

    def predecessor(self, value, strict=False):
        """
        Finds the largest node smaller than or equal to value.
        :param value: y-coordinate value to find predecessor for.
        :param strict: If True, finds strictly smaller value.
        :return: Predecessor TreeNode or None.
        """
        result = None
        current = self.root
        while current:
            if current.value.y < value or (not strict and current.value.y == value):
                result = current
                current = current.right
            else:
                current = current.left
        return result

    def print_inorder(self, node):
        """
        Performs an in-order traversal of the BST and prints each Point.
        For testing purposes only.
        :param node: current node.
        """
        if node is not None:
            self.print_inorder(node.left)  # Visit left subtree
            print(node.value)         # Print current node (Point object)
            self.print_inorder(node.right)  # Visit right subtree


def main():
    # Collects the points to be read from the standard input stream
    data = sys.stdin.read().splitlines()

    # Creates a list of the points that is sorted by the x value
    points = [Point(*map(float, line.split())) for line in data]

    # sort the points based on the x value
    points.sort(key=cmp_to_key(compare_x_value))

    # Calculates the shortest distance between points and prints the value
    distance = closest_distance_sweep_line(points)
    print("The closest pair of points is", distance)


main()
