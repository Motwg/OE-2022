from random import uniform
import math
import sys

from optimization_functions import OptimizationFunction

MIN_INT = -sys.maxsize - 1


class PSO:

    def __init__(self, population, dimension, opt_function, w=[1, 1, 1]):
        assert isinstance(opt_function, OptimizationFunction)

        if opt_function.dimension_constraints[0] > dimension \
                or opt_function.dimension_constraints[1] < dimension:
            raise Exception(f'Given dimension is out of boundaries: '
                            f'{dimension} not in {opt_function.dimension_constraints}')

        self.particles = [{
            'v': [0] * dimension,
            # local max
            'best_local': [0] * dimension,
            # actual position of particle in dimension
            'x': [uniform(*opt_function.x_range) for _ in range(dimension)]
        } for _ in range(population)]
        # global max
        self.best_global = [0] * dimension

        self.w_v = w[0]
        self.w_local = w[1]
        self.w_global = w[2]

        self.opt_fun = opt_function
        self.y = MIN_INT

    def step(self, *args, **kwargs):
        # TODO: AL - implement standard equation listed below
        # v ← ω_v * v + φl*w_l(best_l - x) + φg*w_g(best_g - x)
        # φl and φg are some random variables - for now should be omitted
        # accuracy and x_range can be get via function.accuracy and function.x_range
        # remember that x values can't be lower/greater than x_range
        pass

    def alt_step(self, *args, **kwargs):
        # TODO: AL - implement own equation modification
        pass

    def evaluate(self, iterations=None, alternative=False, *args, **kwargs):
        # accuracy mode
        if iterations is None:
            while True:
                y = self.y
                if alternative:
                    self.alt_step()
                else:
                    self.step()
                if math.fabs(self.y - y) <= self.opt_fun.accuracy:
                    return self.y

        # iteration mode
        elif isinstance(iterations, int) and iterations > 0:
            for _ in range(iterations):
                if alternative:
                    self.alt_step()
                else:
                    self.step()
            return self.y
        else:
            raise Exception(f'Iterations should be integer or left empty, got {iterations}')
