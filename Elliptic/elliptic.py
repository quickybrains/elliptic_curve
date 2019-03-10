"""
    Module contains probabilistic functions
    that could be usefull in elliptic cryptography

"""

from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from random import randint, seed
from numpy import array
from simplicityTests import ferma_test, euler_criterion, root_computation, find_representation, find_quadratic_noncall


# Function finds discriminant of a curve function with given parameters
def find_discriminant(a_value, b_value, field):

    """
    Function finds an discriminant of a cubic function of the following form:
    y^2 = x^3 + a*x + b
    Discriminant may be found with next formula:
    4*a^3 + 27*b^2

    :param int a_value: x coefficient
    :param int b_value: free member
    :param int field: an a curve field

    """

    return (4 * (a_value ** 3) + 27 * (b_value ** 2)) % field


# Function determine if a curve with given parameteres exist
def is_curve_exist(a_value, b_value, field, rounds=None):

    """
    Function determines whether a cubic function (y^2 = x^3 + a*x + b) is exist:

    :param int a_value: x coefficient
    :param int b_value: free member
    :param int field: an a curve field
    :param int rounds: iteration number (optional)

    """

    # Initializing round value for simplicity test
    r = int(7)
    if rounds is not None:
        r = rounds

    # Checking if given field is a simple value
    if ferma_test(field, r) is not True:
        return ValueError, "Given field is not an a simple number"

    # Find discriminant to ensure that a curve exist
    if find_discriminant(a_value, b_value, field) == 0:
        return ValueError, "Given curve doesn't exist"
    else:
        return True


def find_ordinate(x_value, a_value, b_value, field):

    return (x_value**3 + a_value*x_value + b_value) % field


def find_points(a_value, b_value, field):

    points_dict = defaultdict(list)

    for x_value in range(field):
        y_value = find_ordinate(x_value, a_value, b_value, field)
        if y_value == 0:
            points_dict[x_value].append(y_value)
        else:
            try:
                roots = root_computation(y_value, field)
                for point in roots:
                    points_dict[x_value].append(point)
            except TypeError:
                pass

    return points_dict


if __name__ == "__main__":
    pass


