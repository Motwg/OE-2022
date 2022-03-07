import pytest

from optimization_functions import OptimizationFunction


@pytest.fixture
def opt_funct():
    def _make_opt_fun(fun_id):
        return OptimizationFunction(fun_id)
    return _make_opt_fun
