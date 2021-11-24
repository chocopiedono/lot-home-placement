import copy
import math
from collections import deque
import numpy as np


def is_home_valid(home):
    if home is None or len(home) == 0:
        raise ValueError("Home blueprint is None or empty!")

    for el in home:
        if el < 1:
            raise ValueError("Home blueprint has incorrect values")

    # not checking for int home els max values because python3 is not limited here


def is_lot_boundaries_valid(lot_boundaries):
    if lot_boundaries is None or len(lot_boundaries) == 0:
        raise ValueError("Lot's boundaries list is None or empty!")

    for el in lot_boundaries:
        if el is None or len(el) < 2 or el[0] is None or el[1] is None or el[0] < 0 or el[1] < 0 or el[0] > 99 or el[1] > 99:
            raise ValueError("Lot's boundaries have incorrect values")

    # assuming that coordinates of the platform start at 0, 0 and end at 99, 99


def is_rect_fits(rectangular_1: list, rectangular_2: list) -> bool:
    # rectangular_1 - smaller one, rectangular_2 - bigger one
    # formula https://www.jstor.org/stable/2691523

    p = rectangular_1[0]
    q = rectangular_1[1]

    # arrange the notation
    if q > p:
        tmp = q
        q = p
        p = tmp

    a = rectangular_2[0]
    b = rectangular_2[1]

    # arrange the notation
    if a < b:
        tmp = b
        b = a
        a = tmp

    # rectangular case
    if p <= a:
        if q <= b:
            return True
    else:
        diag = ((2 * p * q * a) + (math.pow(p, 2) - math.pow(q, 2)) * math.sqrt(math.pow(p, 2) + math.pow(q, 2) - math.pow(a, 2))) / (math.pow(p, 2) + math.pow(q, 2))
        if b >= diag and q <= b:
            return True

    # if q <= b and (p <= a or b * (p*p+q*q) >= (2*p*q*a + (p*p-q*q) * math.sqrt(p*p+q*q-a*a))):
    #     return True

    return False


def get_largest_rectangular(rectilinear_rectangle: list) -> list:
    # TODO: swap it to the real-world polygon implementation

    matrix = initialize_matrix(rectilinear_rectangle)
    print(matrix)
    rect = get_biggest_rect(matrix)
    print(rect)

    return rect


def initialize_matrix(r_rectangle: list) -> list:

    x = 0
    y = 0

    for coordinate in r_rectangle:
        if coordinate[0] > x:
            x = coordinate[0]
        if coordinate[1] > y:
            y = coordinate[1]

    matrix = np.zeros((x + 1, y + 1))
    np.add.at(matrix, tuple(zip(*r_rectangle)), 1)
    np.rot90(matrix)
    result = np.array(matrix)

    # this part runs in O(N + width * height) time - we have to iterate through N coordinates to find the max x and y
    # also we would iterate through them again to fill the matrix
    # O(width * height) additional space for the matrix itself

    return result


def get_biggest_rect(matrix) -> list:

    # this part runs in O(width * height) time because we have to iterate through every element in the matrix to put
    # it in the stack, cleaning of the stack is insignificant

    width = len(matrix[0])
    height = len(matrix)

    # max depths
    max_matrix = [[None for v in row] for row in matrix]

    def get_max(i, j):
        if i >= width:
            return 0, 0
        elif j >= height:
            return 0, 0
        elif max_matrix[j][i] is not None:
            return max_matrix[j][i]
        elif matrix[j][i] == 0:
            max_matrix[j][i] = (0, 0)
            return max_matrix[j][i]

        max_down = get_max(i, j + 1)
        max_right = get_max(i + 1, j)

        max_matrix[j][i] = (max_right[0] + 1, max_down[1] + 1)
        return max_matrix[j][i]

    def get_rect(stack, j):
        cur_idx = stack.pop()
        cur_max = cur_idx[1] * (j - cur_idx[0])
        # print(f"cur_max at {cur_idx[0]}: {cur_max}")
        return cur_max, cur_idx[1], j - cur_idx[0]

    max_rect = 0
    max_rect_h = 0
    max_rect_w = 0
    for i in range(width):

        # implement the algorithm with stack
        stack = deque()
        stack.append((-1, 0))
        for j in range(height):
            rect = get_max(i, j)
            cur_width = rect[0]
            cur_idx = j
            while stack[-1][1] > cur_width:
                cur_idx = stack[-1][0]
                max_rect = max(max_rect,
                               get_rect(stack, j)[0])
            stack.append((cur_idx, cur_width))

        while len(stack) > 1:
            c_max, c_width, c_height = get_rect(stack, height)
            if c_max > max_rect:
                max_rect_h = c_height
                max_rect_w = c_width
                max_rect = c_max

    return [max_rect_h, max_rect_w]


def apply_setback(home: list, setbacks: int) -> list:
    home_w_setbacks = copy.deepcopy(home)
    home_w_setbacks[0] = home[0] + (setbacks * 2)
    home_w_setbacks[1] = home[1] + (setbacks * 2)
    return home_w_setbacks


def is_compatible(home: list, lot_boundaries: list, setbacks: int) -> bool:

    is_home_valid(home)
    is_lot_boundaries_valid(lot_boundaries)

    # if setback is an equivalent of CSS padding than we will increase the size of the home in the blueprint and
    # calculate accordingly

    home_w_sb = apply_setback(home, setbacks)
    largest_rectangular = get_largest_rectangular(lot_boundaries)

    return is_rect_fits(home_w_sb, largest_rectangular)




