import random
import pytest
from PSO import PSO


def test_pso(sum_opt_funct):
    population = 5
    dimension = 2
    pso = PSO(population, dimension, sum_opt_funct)
    assert isinstance(pso, PSO)
    assert len(pso.particles) == population
    assert len(pso.best_global) == dimension
    assert callable(pso.opt_fun)
    for _ in range(20):
        assert random.uniform(-1e10, 1e10) <= pso.y
    for particle in pso.particles:
        assert isinstance(particle['v'], list)
        assert len(particle['v']) == dimension

        assert isinstance(particle['best_local'], list)
        assert len(particle['best_local']) == dimension
        for b_l in particle['best_local']:
            assert sum_opt_funct.x_range[0] <= b_l <= sum_opt_funct.x_range[1]

        assert isinstance(particle['x'], list)
        assert len(particle['x']) == dimension
        for x in particle['x']:
            assert sum_opt_funct.x_range[0] <= x <= sum_opt_funct.x_range[1]


def test_pso_evaluate(sum_opt_funct):
    pso = PSO(5, 2, sum_opt_funct)
    with pytest.raises(Exception):
        pso.evaluate(iterations=0)
    # sum of 2 dimensions from (-10, 10)
    assert -20 <= pso.evaluate() <= 20
    assert -20 <= pso.evaluate(iterations=50) <= 20
    assert -20 <= pso.evaluate(alternative=True) <= 20
    assert -20 <= pso.evaluate(iterations=50, alternative=True) <= 20
