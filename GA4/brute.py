import full_algorithm
import numpy as np
import random
from pysat.formula import CNF
from pysat.solvers import Solver
import math

IN_PATH = 'in.txt'
OUT_PATH = 'out.txt'

def _generate_problem():
    while True:
        # Mostly produces unsat if greater
        n = random.randint(1, 10)
        m = random.randint(1, 10)
        lights = np.random.randint(np.zeros(m), 2)
        # Maybe should start at zero
        light_connections = np.random.randint(np.zeros((m, 2)), n)
        connections = [[] for _ in range(n)]
        for i, connection in enumerate(light_connections):
            light = i + 1
            connections[connection[0]].append(light)
            connections[connection[1]].append(light)

        connections = [np.array(connection) for connection in connections if len(connection) > 0]

        if len(connections) == n:
            break

    return n, m, lights, connections


def generate_problem():
    return (_generate_problem(), _generate_problem())


def _generate_solution(problem):
    n, m, lights, connections = problem

    light_connections = [[] for _ in range(m)]
    for i, connection in enumerate(connections):
        switch = i + 1
        for light in connection:
            light_connections[light - 1].append(switch)

    clauses = []
    for light, (a, b) in zip(lights, light_connections):
        a = int(a)
        b = int(b)
        if light == 1:
            clauses.append((a, b))
            clauses.append((-a, -b))
        else:
            clauses.append((-a, b))
            clauses.append((a, -b))

    with Solver(bootstrap_with=CNF(from_clauses=clauses)) as solver:
        solution = solver.solve()

    return solution


def generate_solution(problem):
    return (_generate_solution(problem[0]), _generate_solution(problem[1]))


def _write_problem(problem, file):
    n, m, lights, connections = problem
    file.write('***\n')
    file.write(f'{n},{m}\n')
    file.write(np.array2string(lights, separator=',', max_line_width=math.inf)[1:-1].replace(' ', ''))
    file.write('\n')
    for connection in connections:
        file.write(np.array2string(connection, separator=',', max_line_width=math.inf)[1:-1].replace(' ', ''))
        file.write('\n')


def write_problem(problem):
    with open(IN_PATH, 'w+') as file:
        _write_problem(problem[0], file)
        _write_problem(problem[1], file)


problem = generate_problem()
write_problem(problem)
full_algorithm.can_turn_off_lights(IN_PATH, OUT_PATH)

while True:
    print('Checking')

    problem = generate_problem()
    solution = generate_solution(problem)

    write_problem(problem)
    full_algorithm.can_turn_off_lights(IN_PATH, OUT_PATH)

    with open(OUT_PATH, 'r') as file:
        lines = file.readlines()

    failed = False
    for line, sub_solution in list(zip(lines, solution)):
        line = line.strip()
        if (sub_solution and line != 'yes') or (not sub_solution and line != 'no'):
            failed = True
            break

    print(solution)

    if failed:
        print(problem)
        print(solution)
        break
