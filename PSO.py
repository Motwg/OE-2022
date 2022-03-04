from random import uniform
from optimization_functions import OptimizationFunction


class PSO:

    # TODO: implement more initialisation versions
    def __init__(self, population, dimension, x_range):
        self.particles = [{
            # velocity and coefficient of particle
            'v': 0,
            'w_v': 1,
            # local min/max (to ask) with coefficient
            'best_local': 0,
            'w_local': 1,
            # actual position of particle in dimension
            'x': [uniform(x_range[0], x_range[1]) for _ in range(dimension)]
        } for _ in range(population)]
        # w_v and w_local may be shared between all particles or different

        # global min/max (to ask) with coefficient
        self.best_global = 0
        self.w_global = 1

    def __call__(self, function, method, *args, **kwargs):
        assert isinstance(function, OptimizationFunction)

        # TODO: Check once(!) dimension with dimension constraints (from function.dimension_constraints)
        # TODO: Replace pass-es
        # v ← ω_v * v + φl*w_l(l - x) + φg*w_g(best_g - x)
        # φl and φg are some random variables - for now should be omitted
        # accuracy and x_range can be get via function.accuracy and function.x_range
        # remember that x values can't be lower/greater than x_range
        if method == 'iterations':
            pass
        elif method == 'accuracy':
            pass
        else:
            pass
