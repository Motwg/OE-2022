from random import uniform
import math
import sys

from optimization_functions import OptimizationFunction

MAX_FLOAT = float('inf')


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
            'best_local': [uniform(*opt_function.x_range) for _ in range(dimension)],
            # actual position of particle in dimension
            'x': [uniform(*opt_function.x_range) for _ in range(dimension)]
        } for _ in range(population)]
        # global max
        self.best_global = [0] * dimension

        self.w_v = w[0]
        self.w_local = w[1]
        self.w_global = w[2]

        self.opt_fun = opt_function
        self.dimensions = dimension
        self.y = MAX_FLOAT

    def step(self, *args, **kwargs):
        for pn in self.particles:
            for d in range(self.dimensions):
                # Calculate new velocity
                v = self.w_v * pn['v'][d] \
                    + 1.494 * uniform(0, 1) * (pn['best_local'][d] - pn['x'][d]) \
                    + 1.494 * uniform(0, 1) * (self.best_global[d] - pn['x'][d])
                pn['v'][d] = v

                # Check for edge
                new_x_d = pn['x'][d] + v
                if new_x_d < self.opt_fun.x_range[0]:
                    new_x_d = self.opt_fun.x_range[0]
                if new_x_d > self.opt_fun.x_range[1]:
                    new_x_d = self.opt_fun.x_range[1]

                # Change position
                pn['x'][d] = new_x_d

            # Calculate global and local best
            f_value = self.opt_fun(pn['x'])
            best_local_val = self.opt_fun(pn['best_local'])
            best_global_val = self.y

            # Check if value is new local or global minimum
            if f_value < best_global_val:
                self.best_global = pn['x']
            if f_value < best_local_val:
                pn['best_local'] = pn['x']

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
