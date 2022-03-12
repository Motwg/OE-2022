from random import uniform
import math
import sys

from optimization_functions import OptimizationFunction

MAX_FLOAT = float('inf')


class PSO:

    def __init__(self, population, dimension, opt_function, **kwargs):
        assert isinstance(opt_function, OptimizationFunction)

        if opt_function.dimension_constraints[0] > dimension \
                or opt_function.dimension_constraints[1] < dimension:
            raise Exception(f'Given dimension is out of boundaries: '
                            f'{dimension} not in {opt_function.dimension_constraints}')

        self.particles = [{
            'v': [0] * dimension,
            # actual position of particle in dimension
            'x': [uniform(*opt_function.x_range) for _ in range(dimension)]
        } for _ in range(population)]

        # local max
        for p in self.particles:
            p['best_local'] = p['x'].copy()
        # global max
        self.best_global = self.particles[0]['x'].copy()

        self.w_v = kwargs.get('w_v', 1)
        self.w_l = kwargs.get('w_l', 1.494)
        self.w_g = kwargs.get('w_g', 1.494)

        self.opt_fun = opt_function
        self.dimensions = dimension
        self.y = MAX_FLOAT

    def step(self, *args, **kwargs):
        for pn in self.particles:
            for d in range(self.dimensions):
                # Calculate new velocity
                v = self.w_v * pn['v'][d] \
                    + self.w_l * uniform(0, 1) * (pn['best_local'][d] - pn['x'][d]) \
                    + self.w_g * uniform(0, 1) * (self.best_global[d] - pn['x'][d])
                pn['v'][d] = v

                # Check for edge
                new_x_d = pn['x'][d] + v
                if new_x_d < self.opt_fun.x_range[0]:
                    new_x_d = self.opt_fun.x_range[0]
                if new_x_d > self.opt_fun.x_range[1]:
                    new_x_d = self.opt_fun.x_range[1]

                # Change position
                pn['x'][d] = new_x_d

            # Calculate new value
            f_value = self.opt_fun(pn['x'])

            # Check if value is new global minimum
            if f_value < self.y:
                self.best_global = pn['x'].copy()
                self.y = f_value

            # Check if value is new local minimum
            if f_value < self.opt_fun(pn['best_local']):
                pn['best_local'] = pn['x'].copy()

    def alt_step(self, *args, **kwargs):
        for pn in self.particles:
            for d in range(self.dimensions):
                # Calculate new velocity
                v = self.w_v * pn['v'][d] \
                    + (self.w_l * uniform(0, 1) * (pn['best_local'][d] - pn['x'][d])**2
                       + self.w_g * uniform(0, 1) * (self.best_global[d] - pn['x'][d])**2)**0.5
                pn['v'][d] = v

                # Check for edge
                new_x_d = pn['x'][d] + v
                if new_x_d < self.opt_fun.x_range[0]:
                    new_x_d = self.opt_fun.x_range[0]
                if new_x_d > self.opt_fun.x_range[1]:
                    new_x_d = self.opt_fun.x_range[1]

                # Change position
                pn['x'][d] = new_x_d

            # Calculate new value
            f_value = self.opt_fun(pn['x'])

            # Check if value is new global minimum
            if f_value < self.y:
                self.best_global = pn['x'].copy()
                self.y = f_value

            # Check if value is new local minimum
            if f_value < self.opt_fun(pn['best_local']):
                pn['best_local'] = pn['x'].copy()

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
