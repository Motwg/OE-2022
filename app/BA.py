from functools import partial
from random import uniform

from app.SO import SO
from app.utils import bounce


def call_w(w):
    """if 'w' looks like [*args] call uniform with args"""
    if isinstance(w, (tuple, list)):
        return uniform(*w)
    return w


class BA(SO):

    def __init__(self, population, dimension, opt_function, **kwargs):
        super().__init__(population, dimension, opt_function)

        self.bats = {}

        # feed bounce function with constant x_range to speed up computing
        self.bounce = partial(bounce, x_range=self.opt_fun.x_range)
        self.f_range = kwargs.get('freq_range', (0, 2))

        self.reset()

    def count_freq(self):
        return self.f_range[0] + uniform(0, 1) * (self.f_range[1] - self.f_range[0])

    def step(self) -> float:

        for bat in self.bats:
            # calculate vectors of velocity and position
            bat['v'] = list(map(
                lambda v, x: v + self.count_freq() * (x - self.best_global),
                bat['v'], bat['x']
            ))
            bat['x'] = list(map(
                lambda v, x: self.bounce(x + v),
                bat['v'], bat['x']
            ))
            if uniform(0, 1) > bat['r']:
                best_global = list(map(
                    lambda x: uniform(-1, 1) * self.count_avg_loudness(),
                    self.best_global
                ))
                y = self.opt_fun(best_global)
                if y < self.y and uniform(0, 1) < bat['A']:
                    self.y = y
                    self.best_global = best_global

        return self.y

    def rate_bat(self, bat):
        bat['y'] = self.opt_fun(bat['x'])
        if bat['y'] < self.y:
            self.y = bat['y']
            self.best_global = bat['x']

    def count_avg_loudness(self):
        return sum(bat['A'] for bat in self.bats) / len(self.bats)

    def evaluate(self, iterations=None, *args, **kwargs):
        return super().evaluate(self.step, iterations)

    def reset(self):
        super().reset()

        self.bats = [{
            'v': [0] * self.dimensions,
            # actual position of particle in dimension
            'x': [uniform(*self.opt_fun.x_range) for _ in range(self.dimensions)],
            'A': 0.0,  # loudness
            'r': 0.0  # pulse rate
        } for _ in range(self.population)]

        [self.rate_bat(bat) for bat in self.bats]

        # global max
        self.best_global = self.bats[0]['x']
