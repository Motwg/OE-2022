import json

from PSO import PSO
from optimization_functions import OptimizationFunction


def check_input(predicate, msg, error_string='Input does not exist'):
    while True:
        result = input(msg).strip()
        if predicate(result):
            return result
        print(error_string)


if __name__ == '__main__':
    with open('input.json') as json_file:
        data = json.load(json_file)
    assert isinstance(data, dict)
    [print(f'{k} : {v}') for k, v in data.items() if k.startswith('pso_')]
    input_data = check_input(lambda x: x in data, 'Choose your input: ')
    input_data = data[input_data]
    print(input_data)

    opt_function = OptimizationFunction(input_data['function'])
    pso = PSO(input_data['population'], input_data['dimension'], opt_function.x_range)

    # Tests (I will extract them later)
    print(f'{opt_function([5, 4, 3])} = 50')
    print(pso.step(opt_function))
    print(pso.alt_step(opt_function))
    print(pso.evaluate(opt_function, 'iterations'))
