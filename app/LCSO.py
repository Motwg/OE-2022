from collections import OrderedDict
from random import uniform, sample, choice
from functools import partial

from app.SO import SO
from app.utils import bounce, shuffle, grouped, flatten


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

        # initialises particles splitting them into swarms
        # e.g. [[swarm 0], [swarm 1], ...]; swarms may not be equal in size
        self.particles = [[{
            # random velocity at start
            'v': [uniform(*v_init_range) for _ in range(self.dimensions)],
            'x': [uniform(*self.opt_fun.x_range) for _ in range(self.dimensions)]
        } for _ in range(swarm, self.population, self.no_swarms)]
            for swarm in range(self.no_swarms)]

        # global max
        self.best_global = self.particles[0][0]['x'].copy()

    def step(self) -> float:
        self.shuffle()
        selected_winners = self.stage_one()
        self.stage_two(selected_winners)
        self.select_best()
        return self.y

    def stage_one(self):
        winners = []
        for i, swarm in enumerate(self.particles):
            # select only one random winner particle for each swarm
            winners.append(choice(
                # take every 3 particles from swarm only once and get winners
                [self.tournament([(i, p), (i, p + 1), (i, p + 2)])
                 for p in range(len(swarm) % 3, len(swarm), 3)]
            ))
        return shuffle(winners)

    def stage_two(self, winners):
        # take every 3 particles from swarm only once
        for first, second, third in grouped(winners, 3):
            self.tournament([first, second, third])

    def shuffle(self):
        self.particles = [sample(self.particles[i], k=len(self.particles[i]))
                          for i in range(self.no_swarms)]

    def tournament(self, idx_particles: list) -> tuple:
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

        # compute new position for s and loser
        x = list(map(count_x, w['x'], s['x'], los['x'], s['v'], los['v']))
        # rotate matrix to extract x_s and x_l in vectors
        vector_x_s, vector_x_l = list(zip(*x))

        # perform map to get full vector of x
        s['x'] = list(map(self.bounce, vector_x_s))
        los['x'] = list(map(self.bounce, vector_x_l))

        # return indexes of winner
        return next(iter(ordered))

    def get_particle(self, swarm_idx, particle_idx):
        return self.particles[swarm_idx][particle_idx]

    def select_best(self):
        flattened = flatten(self.particles)
        computed = {i: self.opt_fun(p['x']) for i, p in enumerate(flattened)}
        # find particle with minimal value of optimisation function
        best_particle_idx = min(computed, key=computed.get)
        self.y = computed[best_particle_idx]
        self.best_global = flattened[best_particle_idx]['x']

    def evaluate(self, iterations: int = None, *args, **kwargs):
        return super().evaluate(self.step, iterations)
