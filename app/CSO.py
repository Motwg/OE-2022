import random

from app.SO import SO
from random import uniform


class CSO(SO):

    def __init__(self, population, dimension, opt_function, **kwargs):
        super().__init__(population, dimension, opt_function)
        # TODO: (AL) add needed definitions
        self.particles = {}

        self.reset()

    def reset(self):
        super().reset()
        # TODO: (AL) add needed things to reset after finding solution
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

    def step(self) -> float:
        # TODO: (AL) add implementation

        # Calculate avg position
        sum_pos = [0] * self.dimensions
        avg_pos = [0] * self.dimensions
        for d in range(self.dimensions):
            for pn in self.particles:
                sum_pos[d] += pn['x'][d]
            avg_pos[d] = sum_pos[d]/len(self.particles)

        # Create random pairs
        particles_copy = self.particles.copy()
        pn1 = [0] * self.dimensions
        pn2 = [0] * self.dimensions
        for i in range(int(len(self.particles)/2)):
            index1 = int(random.uniform(0, len(particles_copy)))
            pn1 = particles_copy[index1]
            del particles_copy[index1]
            index2 = int(random.uniform(0, len(particles_copy)))
            pn2 = particles_copy[index2]
            del particles_copy[index2]

        # Particles compete
        f1 = self.opt_fun(pn1['x'])
        f2 = self.opt_fun(pn2['x'])

        # Loser changes parameters
        if f1 > f2:
            self.adjust_loser(pn1, pn2, avg_pos)
        if f1 < f2:
            self.adjust_loser(pn2, pn1, avg_pos)

        if f1 < self.y:
            self.y = f1
            self.best_global = pn1['x'].copy()
        if f2 < self.y:
            self.y = f2
            self.best_global = pn2['x'].copy()

        return self.y

    def evaluate(self, iterations: int = None, *args, **kwargs):
        return super().evaluate(self.step, iterations)

    def adjust_loser(self, pnw, pnl, avg_pos):
        wp = self.get_particle(pnw)
        lp = self.get_particle(pnl)

        w = 0.5

        for d in range(self.dimensions):
            v = uniform(0, 1) * lp['v'][d] \
                   + uniform(0, 1) * (wp['x'][d] - lp['x'][d]) \
                   + w * uniform(0, 1) * (avg_pos[d] - lp['x'][d])

            # Check for edge
            new_x_d = lp['x'][d] + v
            if new_x_d < self.opt_fun.x_range[0]:
                new_x_d = (self.opt_fun.x_range[0] + self.opt_fun.x_range[1]) / 2
            if new_x_d > self.opt_fun.x_range[1]:
                new_x_d = (self.opt_fun.x_range[0] + self.opt_fun.x_range[1]) / 2

            lp['x'][d] = new_x_d

    def get_particle(self, par):
        for pn in self.particles:
            if pn == par:
                return pn
