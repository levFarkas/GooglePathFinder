import math


def l2distance(x, y):
    return math.sqrt(sum([pow(i - j, 2) for (i, j) in zip(x, y)]))
