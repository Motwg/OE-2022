from random import uniform

from optimization_functions import OptimizationFunction


class PSO:

    def __init__(self, population, dimension, x_range, w=[1, 1, 1]):
        # v ← ω_v * v + w_l(best_l - x) + w_g(best_g - x)
        self.particles = [{
            'v': [0] * dimension,
            # local max with coefficient
            'best_local': [0] * dimension,
            # actual position of particle in dimension
            'x': [uniform(x_range[0], x_range[1]) for _ in range(dimension)]
        } for _ in range(population)]
        # global max with coefficient
        self.w_v = w[0]
        self.w_local = w[1]
        self.best_global = [0] * dimension
        self.w_global = w[2]

    def step(self, function, *args, **kwargs):
        assert isinstance(function, OptimizationFunction)
        # TODO: AL - implement standard equation listed below
        # v ← ω_v * v + φl*w_l(best_l - x) + φg*w_g(best_g - x)
        # φl and φg are some random variables - for now should be omitted
        # accuracy and x_range can be get via function.accuracy and function.x_range
        # remember that x values can't be lower/greater than x_range
        pass

    def alt_step(self, function, *args, **kwargs):
        assert isinstance(function, OptimizationFunction)
        # TODO: AL - implement own equation modification
        pass

    def evaluate(self, function, method, *args, **kwargs):
        # TODO: Check once(!) dimension with dimension constraints (from function.dimension_constraints)
        # TODO: Replace pass-es
        if method == 'iterations':
            pass
        elif method == 'accuracy':
            pass
        else:
            pass
