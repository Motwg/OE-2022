import json
import csv

from itertools import zip_longest

from app.GA import GA
from app.PSO import PSO
from app.optimization_functions import OptimizationFunction


def check_input(predicate, msg, error_string='Input does not exist'):
    while True:
        result = input(msg).strip()
        if predicate(result):
            return result
        print(error_string)


def write_csv(filename, headers, csv_data, csv_dir='files'):
    with open(f'{csv_dir}/{filename}', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(csv_data)


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
    y_matrix = []
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
            y_matrix.append(pso.logs['y'])

            print(f'Best solution {pso.y} for {pso.best_global}')
            print(pso.logs)
            pso.reset()
        print(f'Solutions : {y}')
        print(f'Iterations: {iterations}')
        print(f'Average best solution: {sum(y) / repeats}')
        print(f'Average iterations nr: {sum(iterations) // repeats}')

        avg_y.append(sum(y) / repeats)
        avg_iterations.append(sum(iterations) // repeats)

        if data['settings']['activate_ga']:
            y_ga, iterations_ga = [], []
            for i in range(repeats):
                print(f'===REPEAT {i + 1}===')
                ga = GA(
                    input_data['dimension'],
                    opt_function,
                    input_data.get('iterations', 100)
                )
                ga.run()
                solution, solution_fitness = ga.best_solution()
                y_ga.append(solution_fitness)
                iterations_ga.append(input_data.get('iterations', 100))
                print(y_ga)
            write_csv(
                f'ga_{input_data["function"]}.csv',
                (f'ga_{input_data["function"]}_solution',
                 f'ga_{input_data["function"]}_iterations'),
                zip(y_ga, iterations_ga)
            )

        # save to csv y and iterations
        if data['settings']['save_csv_details']:
            variant = user_input.removeprefix('pso_')
            write_csv(
                f'{user_input}.csv',
                (f'{variant}_solution', f'{variant}_iterations'),
                zip(y, iterations)
            )
        # take only actual repeats
        cur_y_matrix = y_matrix[-repeats:]
        # save all y-s in every repeat
        if data['settings']['save_csv_y_matrix']:
            write_csv(
                f'{user_input}_y_matrix.csv',
                range(1, repeats + 1),
                # needs to rotate matrix
                zip_longest(*cur_y_matrix[::-1])
            )
    # save to csv avg_y and avg_iterations for every input
    if data['settings']['save_csv_summary']:
        write_csv(
            'pso.csv',
            ('input', 'avg_y', 'avg_iterations'),
            zip(user_inputs, avg_y, avg_iterations)
        )
