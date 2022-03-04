def fun_switcher(fun_id):
    return {
        'f1': {
            'fun': f1,
            'dimension_constraints': (2, 100),
            'x_range': (-100, 100),
            'accuracy': 0.0001
        },
        'f2': {
            'fun': f2,
            'dimension_constraints': (2, 100),
            'x_range': (-100, 100),
            'accuracy': 0.0001
        },
        'f10': {
            'fun': f10,
            'dimension_constraints': (2, 100),
            'x_range': (-10, 10),
            'accuracy': 0.000001
        }
    }.get(fun_id, 'f1')


def f1(vector_x):
    return sum(x * x for x in vector_x)


def f2(vector_x):
    sum_value = 0
    for i, x in enumerate(vector_x):
        x_i = x - i
        sum_value += x_i * x_i
    return sum_value


def f5(vector_x):
    # TODO: AL
    pass


def f7(vector_x):
    # TODO: AL
    pass


def f10(vector_x):
    # TODO: AL
    pass


# TODO: AL - more functions pls

class OptimizationFunction:
    def __init__(self, opt_function_id: str, **kwargs):
        temp_function = fun_switcher(opt_function_id)
        self.opt_function = temp_function['fun']
        self.dimension_constraints = temp_function['dimension_constraints']
        self.x_range = kwargs.get('x_range', temp_function['x_range'])
        self.accuracy = kwargs.get('accuracy', temp_function['accuracy'])

    def __call__(self, vector_x, *args, **kwargs):
        return self.opt_function(vector_x)
