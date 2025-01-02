import full_algorithm
import numpy as np
import random
from scipy.sparse import csgraph
from scipy.sparse import csr_matrix

IN_PATH = 'in.txt'
OUT_PATH = 'out.txt'

def generate_problem(shape=None):
    if shape is None:
        shape = random.randint(3, 12)
    unsym = np.asarray((1 - np.eye(shape)) * np.random.uniform(0, 3, (shape, shape)), dtype=np.int32)
    # Sqrt
    return np.maximum(unsym, unsym.transpose())


def generate_solution(graph):
    reses = []

    graph = graph.copy() + 1
    edges =  len(graph) - 1
    reses.append(csgraph.minimum_spanning_tree(graph))

    for i in range(len(graph)):
        for j in range(i):
            copy = graph.copy()
            copy[i, j] = 0
            copy[j, i] = 0
            # Could be optimized to removed repeated checks
            for i1 in range(len(graph)):
                for j1 in range(i1):
                    copy1 = copy.copy()
                    copy1[i1, j1] = 0
                    copy1[j1, i1] = 0

                    sol = csgraph.minimum_spanning_tree(copy1)
                    if sol.count_nonzero() == edges:
                        reses.append(sol)

    reses = sorted(reses, key=lambda res: -csr_matrix.sum(res))

    first = reses.pop()

    while True:
        second = reses.pop()
        if (second != first).nnz != 0:
            break

    while True:
        third = reses.pop()
        if (third != second).nnz != 0 and (third != first).nnz != 0:
            break

    return int(csr_matrix.sum(first) - edges), int(csr_matrix.sum(second) - edges), int(csr_matrix.sum(third) - edges)


def write_problem(problem):
    with open(IN_PATH, 'w+') as file:
        file.write(str(len(problem)))
        file.write('\n')
        file.write('\n'.join(','.join(str(num) for num in row) for row in problem))


problem = generate_problem(30)
write_problem(problem)
full_algorithm.three_min_spanning_trees(IN_PATH, OUT_PATH)

while True:
    print('Checking')

    problem = generate_problem()
    solution = generate_solution(problem)

    with open(IN_PATH, 'w+') as file:
        file.write(str(len(problem)))
        file.write('\n')
        file.write('\n'.join(','.join(str(num) for num in row) for row in problem))

    full_algorithm.three_min_spanning_trees(IN_PATH, OUT_PATH)

    with open(OUT_PATH, 'r') as file:
        lines = file.readlines()

    failed = False
    for line, solution_part in list(zip(lines, solution)):
        if int(line.lstrip()) != solution_part:
            failed = True

    if failed:
        print(problem)
        print(solution)
        break
