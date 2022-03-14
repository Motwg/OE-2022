import json
import csv

from app.PSO import PSO
from app.optimization_functions import OptimizationFunction


def check_input(predicate, msg, error_string='Input does not exist'):
    while True:
        result = input(msg).strip()
        if predicate(result):
            return result
        print(error_string)


if __name__ == '__main__':
    with open('files/input.json') as json_file:
        data = json.load(json_file)
    assert isinstance(data, dict)

    # auto pass inputs
    if data['settings']['auto']:
        user_inputs = data['settings']['inputs']
        inputs_data = [data[auto_input] for auto_input in user_inputs]
    else:
        [print(f'{k} : {v}') for k, v in data.items() if k.startswith('pso_')]
        user_inputs = check_input(lambda x: x in data, 'Choose your input: ')
        inputs_data = [data[user_inputs]]

    avg_y, avg_iterations = [], []
    csv_dir = 'files'
    for user_input, input_data in zip(user_inputs, inputs_data):
        print('=' * 100)
        print(input_data)
        # init classes
        opt_function = OptimizationFunction(input_data['function'])
        pso = PSO(
            input_data['population'],
            input_data['dimension'],
            opt_function,
            **data["w_parameters"][input_data['w_set']]
        )

        y, iterations = [], []
        repeats = data['settings']['repeats']
        for i in range(repeats):
            print(f'===REPEAT {i + 1}===')

            y.append(pso.evaluate(
                iterations=input_data.get('iterations', None),
                alternative=input_data.get('alternative', False)
            ))
            iterations.append(pso.logs['iterations'])

            print(f'Best solution {pso.y} for {pso.best_global}')
            print(pso.logs)
            pso.reset()
        print(f'Solutions : {y}')
        print(f'Iterations: {iterations}')
        print(f'Average best solution: {sum(y) / repeats}')
        print(f'Average iterations nr: {sum(iterations) // repeats}')

        avg_y.append(sum(y) / repeats)
        avg_iterations.append(sum(iterations) // repeats)

        # print('===GA===')
        # ga = GA(input_data['dimension'], opt_function, 100)
        # ga.run()
        # solution, solution_fitness = ga.best_solution()
        # print(f'Parameters of the best solution : {solution}')
        # print(f'Fitness value of the best solution = {solution_fitness}')

        # save to csv y and iterations
        if data['settings']['save_csv_details']:

            variant = user_input.removeprefix('pso_')
            with open(f'{csv_dir}/{user_input}.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow((f'{variant}_solution', f'{variant}_iterations'))
                writer.writerows(zip(y, iterations))

    # save to csv avg_y and avg_iterations for every input
    if data['settings']['save_csv_summary']:
        with open(f'{csv_dir}/pso.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('input', 'avg_y', 'avg_iterations'))
            writer.writerows(zip(user_inputs, avg_y, avg_iterations))
