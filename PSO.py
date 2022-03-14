from random import uniform
import math
import sys

from optimization_functions import OptimizationFunction

MAX_FLOAT = float('inf')


def call_w(w):
    """if 'w' looks like [function, *args] call function with args"""
    if isinstance(w, (tuple, list)) and callable(w[0]):
        return w[0](*w[1:])
    return w


class PSO:

    def __init__(self, population, dimension, opt_function, **kwargs):
        assert isinstance(opt_function, OptimizationFunction)

        if opt_function.dimension_constraints[0] > dimension \
                or opt_function.dimension_constraints[1] < dimension:
            raise Exception(f'Given dimension is out of boundaries: '
                            f'{dimension} not in {opt_function.dimension_constraints}')
        self.particles = {}
        self.best_global = []

        self.w_v = kwargs.get('w_v', 0.729)
        self.w_l = kwargs.get('w_l', 1.494)
        self.w_g = kwargs.get('w_g', 1.494)

        self.opt_fun = opt_function
        self.dimensions = dimension
        self.population = population
        self.y = MAX_FLOAT

        self.logs = {}

        self.reset()

    def step(self, *args, **kwargs):
        for pn in self.particles:
            for d in range(self.dimensions):
                # Calculate new velocity
                v = call_w(self.w_v) * pn['v'][d] \
                    + call_w(self.w_l) * uniform(0, 1) * (pn['best_local'][d] - pn['x'][d]) \
                    + call_w(self.w_g) * uniform(0, 1) * (self.best_global[d] - pn['x'][d])
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
        avg_diff = [0] * self.dimensions
        for d in range(self.dimensions):
            for pn in self.particles:
                avg_diff[d] += self.best_global[d] - pn['x'][d]
            avg_diff[d] /= len(self.particles)

        for pn in self.particles:
            for d in range(self.dimensions):
                # Calculate new velocity
                v = call_w(self.w_v) * pn['v'][d] \
                    + call_w(self.w_l) * uniform(0, 1) * (pn['best_local'][d] - pn['x'][d]) \
                    + call_w(self.w_g) * uniform(0, 1) * (avg_diff[d] - pn['x'][d])
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
        logs_y = []
        # accuracy mode
        if iterations is None:
            for i in range(10000):
                y = self.y
                if alternative:
                    self.alt_step()
                else:
                    self.step()
                logs_y.append(self.y)
                if 0 < math.fabs(self.y - y) <= self.opt_fun.accuracy:
                    self.logs['iterations'] = i
                    break

        # iteration mode
        elif isinstance(iterations, int) and iterations > 0:
            for i in range(iterations):
                if alternative:
                    self.alt_step()
                else:
                    self.step()
                logs_y.append(self.y)
            self.logs['iterations'] = iterations
        else:
            raise Exception(f'Iterations should be integer or left empty, got {iterations}')

        self.logs['avg_y'] = sum(logs_y) / len(self.particles)
        self.logs['y'] = tuple(logs_y)
        return self.y

    def reset(self):
        self.particles = [{
            'v': [0] * self.dimensions,
            # actual position of particle in dimension
            'x': [uniform(*self.opt_fun.x_range) for _ in range(self.dimensions)]
        } for _ in range(self.population)]

        # local max
        for p in self.particles:
            p['best_local'] = p['x'].copy()
        # global max
        self.best_global = self.particles[0]['x'].copy()

        self.y = MAX_FLOAT

        self.logs = {}
