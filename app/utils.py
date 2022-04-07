from random import sample
from functools import reduce
from operator import concat


def bounce(x, x_range):
    # TODO: Make it bounce instead of glueing
    return glue_to_wall(x, x_range)


def glue_to_wall(x, x_range):
    if x < x_range[0]:
        return x_range[0]
    elif x > x_range[1]:
        return x_range[1]
    else:
        return x


def shuffle(iterable):
    return sample(iterable, k=len(iterable))


def grouped(iterable, n):
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), ..."""
    return zip(*[iter(iterable)] * n)


def flatten(iterable):
    """((s00, s01), (s10, s11), ...) -> (s00, s01, s10, s11, ...)"""
    return reduce(concat, iterable)
