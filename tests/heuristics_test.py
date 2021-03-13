import math
from itertools import product

from GooglePathFinder.src.heuristics import l2distance

###############################################################################
# Utility functions

# Generate scalars in the form of [[x11,...,x1n],[x21,...,x2n],...]
def scalar_generator(dimensions=2):
    dim = [[-2, 1, 0, 1, 2]] * dimensions
    scalars = list(product(*dim))

    def generator():
        for i in range(len(scalars)):
            yield scalars[i]

    return generator


# Check a property of a scalar
def scalar_tester(property_assertion):
    def scalar_tester():
        x_generator = scalar_generator()
        for x in x_generator():
            assert property_assertion(x)
            print(f"Assertion passed: {x}")

    return scalar_tester


# Check a property of multiple scalars
def multi_scalar_tester(num_scalars):
    def multi_scalar_tester_factory(property_assertion):
        def scalar_tester():
            generator_list = [scalar_generator()() for i in range(num_scalars)]
            prod = product(*generator_list)

            for p in prod:
                assert property_assertion(*[p[i] for i in range(num_scalars)])
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
