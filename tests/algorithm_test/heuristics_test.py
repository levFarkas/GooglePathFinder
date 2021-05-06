import math
from itertools import product

from src.algorithm.heuristics import l2distance


###############################################################################
# Utility functions

# Generate scalars in the form of [[x11,...,x1n],[x21,...,x2n],...]
# All permutations are generated of the predefined values
def scalar_generator(dimensions=2):
    base = [[-2, 1, 0, 1, 2]] * dimensions
    permutations = list(product(*base))

    def generator():
        for i in range(len(permutations)):
            yield permutations[i]

    return generator


# Check a criteria for one scalar
def scalar_tester(criteria_function):
    def scalar_tester():
        x_generator = scalar_generator()
        for x in x_generator():
            assert criteria_function(x)
            print(f"Assertion passed: {x}")

    return scalar_tester


# Check a criteria for multiple scalars
def multi_scalar_tester(num_scalars):
    def multi_scalar_tester_factory(criteria_function):
        def scalar_tester():
            generator_list = [scalar_generator()() for i in range(num_scalars)]
            prod = product(*generator_list)

            for p in prod:
                assert criteria_function(*[p[i] for i in range(num_scalars)])
                print(f"Assertion passed: {[p[i] for i in range(num_scalars)]}")

        return scalar_tester

    return multi_scalar_tester_factory


###############################################################################
# Test l2distance (based on the definition of 'mertic spaces')


@multi_scalar_tester(2)
def test_l2distance_non_negative(x, y):
    return l2distance(x, y) >= 0


@scalar_tester
def test_l2distance_non_degenerate(x):
    return l2distance(x, x) == 0


@multi_scalar_tester(2)
def test_l2distance_symmetric(x, y):
    return l2distance(x, y) == l2distance(y, x)


@multi_scalar_tester(3)
def test_triangle_inequality(x, y, z):
    return l2distance(x, z) <= l2distance(x, y) + l2distance(y, z) or math.isclose(
        l2distance(x, z), l2distance(x, y) + l2distance(y, z)
    )
