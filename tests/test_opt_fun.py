import pytest


def test_f1(opt_funct):
    f = opt_funct('f1')
    assert f([5, 4, 3]) == 50
    assert f([1.2, 2.4, 3.4]) == pytest.approx(18.76, 0.1)
    assert f([]) == 0
    with pytest.raises(TypeError):
        f(3)
    with pytest.raises(TypeError):
        f('ok')
    with pytest.raises(TypeError):
        f(None)
        
        
def test_f2(opt_funct):
    f = opt_funct('f2')
    assert f([5, 4, 3]) == 35
    assert f([1.2, 2.4, 3.4]) == pytest.approx(5.36, 0.1)
    assert f([]) == 0
    with pytest.raises(TypeError):
        f(3)
    with pytest.raises(TypeError):
        f('ok')
    with pytest.raises(TypeError):
        f(None)
