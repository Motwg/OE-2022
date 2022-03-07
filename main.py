import json

from GA import GA
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
    pso = PSO(input_data['population'], input_data['dimension'], opt_function)

    print(pso.step())
    print(pso.alt_step())

    print(pso.particles[0])

    print('===GA===')
    ga = GA(input_data['dimension'], opt_function, 100)
    ga.run()
    solution, solution_fitness = ga.best_solution()
    print(f'Parameters of the best solution : {solution}')
    print(f'Fitness value of the best solution = {solution_fitness}')
