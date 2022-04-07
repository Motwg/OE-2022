from functools import partial
from random import uniform, sample, choices

from app.SO import SO
from app.utils import bounce


class CSO(SO):

    def __init__(self, population, dimension, opt_function, **kwargs):
        super().__init__(population, dimension, opt_function)

        self.particles = {}
        self.velocity_magnitude = kwargs.get('velocity_magnitude', 0.0)

        # feed bounce function with constant x_range to speed up computing
        self.bounce = partial(bounce, x_range=self.opt_fun.x_range)

        self.reset()

    def reset(self):
        super().reset()

        # (x_range difference * -magnitude, x_range difference * magnitude)
        v_init_range = list(map(
            lambda m: (self.opt_fun.x_range[1] - self.opt_fun.x_range[0]) * m,
            (-self.velocity_magnitude, self.velocity_magnitude)
        ))

        self.particles = [{
            'v': [uniform(*v_init_range) for _ in range(self.dimensions)],
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
            avg_pos[d] = sum_pos[d] / len(self.particles)

        # Make copy of particles
        particles_copy = self.particles.copy()

        for i in range(len(self.particles) // 2):
            # Select random two particles
            pn1, pn2 = sample(particles_copy, k=2)
            # Delete them from copy set
            del particles_copy[self.get_particle_index(particles_copy, pn1)]
            del particles_copy[self.get_particle_index(particles_copy, pn2)]
            # Particles compete
            f1 = self.opt_fun(pn1['x'])
            f2 = self.opt_fun(pn2['x'])
            # Loser changes parameters
            if f1 > f2:
                self.adjust_loser(pn1, pn2, avg_pos)
            elif f1 < f2:
                self.adjust_loser(pn2, pn1, avg_pos)
            # Assign new values if new minimum
            if f1 < self.y:
                self.y = f1
                self.best_global = pn1['x'].copy()
            elif f2 < self.y:
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

    def get_particle_index(self, copy_set, par):
        for i in range(len(copy_set)):
            if copy_set[i] == par:
                return i
