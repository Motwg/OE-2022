from collections import OrderedDict
from random import uniform, choices
from functools import partial

from app.SO import SO
from app.utils import bounce


def validate_lcso(init):
    """
    Validates LCSO inputs in init
    """

    def wrapper(self, population, dimension, opt_function, no_swarms, **kwargs):
        if no_swarms < 3:
            raise Exception(f'Number of swarms should be greater than 2, '
                            f'got {no_swarms}')
        elif population < 3 * no_swarms:
            raise Exception(f'Population should be 3 times greater than number of swarms, '
                            f'got {population} < {no_swarms}')
        return init(self, population, dimension, opt_function, no_swarms, **kwargs)

    return wrapper


class LCSO(SO):

    @validate_lcso
    def __init__(self, population, dimension, opt_function, no_swarms, **kwargs):
        super().__init__(population, dimension, opt_function)
        self.particles = []
        self.no_swarms = no_swarms

        self.reset()

    def reset(self):
        super().reset()

        # initialises particles splitting them into swarms
        # e.g. [[swarm 0], [swarm 1], ...]; swarms may not be equal in size
        self.particles = [[{
            'v': [0] * self.dimensions,
            # actual position of particle in dimension
            'x': [uniform(*self.opt_fun.x_range) for _ in range(self.dimensions)]
        } for _ in range(swarm, self.population, self.no_swarms)]
            for swarm in range(self.no_swarms)]

        # local max
        for swarm in self.particles:
            for p in swarm:
                p['best_local'] = p['x'].copy()
        # global max
        self.best_global = self.particles[0][0]['x'].copy()

    def step(self) -> float:
        self.shuffle()
        self.stage_one()
        self.stage_two()
        return self.y

    def stage_one(self):
        for i, swarm in enumerate(self.particles):
            # take every 3 particles from swarm only once
            for p in range(len(swarm) % 3, len(swarm), 3):
                self.tournament([(i, p), (i, p + 1), (i, p + 2)])

    def stage_two(self):
        # TODO:
        pass

    def shuffle(self):
        self.particles = [choices(self.particles[i], k=len(self.particles[i]))
                          for i in range(self.no_swarms)]

    def tournament(self, idx_particles: list):
        # sort ascending indexes by calculated function value
        ordered = OrderedDict(sorted(
            {i: self.get_particle(*i) for i in idx_particles}.items(),
            key=lambda kv: self.opt_fun(kv[1]['x'])
        ))
        # assign particles to w, v and los (these are not copies!)
        w, s, los = ordered.values()

        def count_x(x_w, x_s, x_l, v_s, v_l):
            v_s = uniform(0, 1) * v_s + uniform(0, 1) * (x_w - x_s)
            v_l = uniform(0, 1) * v_l \
                + uniform(0, 1) * (x_w - x_l) \
                + uniform(0, 1) * (x_s - x_l)
            return v_s + x_s, v_l + x_l
        # compute velocity
        v = list(map(count_x, w['x'], s['x'], los['x'], s['v'], los['v']))
        # rotate matrix to extract x_s and x_l in vectors
        vector_x_s, vector_x_l = list(zip(*v))

        # feed bounce function with constant input
        bounce_x_range = partial(bounce, x_range=self.opt_fun.x_range)
        # perform map to get full vector of x
        s['x'] = list(map(bounce_x_range, vector_x_s))
        los['x'] = list(map(bounce_x_range, vector_x_l))

    def get_particle(self, swarm_idx, particle_idx):
        return self.particles[swarm_idx][particle_idx]

    def evaluate(self, iterations: int = None, *args, **kwargs):
        return super().evaluate(self.step, iterations)
