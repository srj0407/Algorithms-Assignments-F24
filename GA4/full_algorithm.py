from collections import defaultdict

neg = '~'


# directed graph class
#  adapted from:
#  src: https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/
class dir_graph:
    def __init__(self):
        # create an empty directed graph, represented by a dictionary
        #  The dictionary consists of keys and corresponding lists
        #  Key = node u , List = nodes, v, such that (u,v) is an edge
        self.graph = defaultdict(set)
        self.nodes = set()

    # Function that adds an edge (u,v) to the graph
    #  It finds the dictionary entry for node u and appends node v to its list
    # performance: O(1)
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.nodes.add(u)
        self.nodes.add(v)

    # Function that outputs the edges of all nodes in the graph
    #  prints all (u,v) in the set of edges of the graoh
    # performance: O(m+n) m = #edges , n = #nodes
    def print(self):
        edges = []
        # for each node in graph
        for node in self.graph:
            # for each neighbour node of a single node
            for neighbour in self.graph[node]:
                # if edge exists then append
                edges.append((node, neighbour))
        return edges


# 2-CNF class
#  Class storing a boolean formula in Conjunctive Normal Form of literals
#  where the size of clauses is at most 2
#  -NOTATION-
#    The CNF is represented as a list of lists
#    e.g [[x, y], [k, z]] == (x or y) and (k or z)
#    i.e Conjunction of inner lists , where the inner lists are disjunctions
#    of literals
#    Negation is represented with ~ .  ~x == negation of literal x
# class two_cnf:
class two_cnf:
    def __init__(self):
        self.con = []

    # adds a clause to the CNF
    # performance O(1)
    def add_clause(self, clause):
        if len(clause) <= 2:
            self.con.append(clause)
        else:
            print("error: clause contains > 2 literals")

    # returns a set of all the variables in the CNF formula
    def get_variables(self):
        vars = set()
        for clause in self.con:
            for literal in clause:
                vars.add(literal)
        return vars

    def print(self):
        print(self.con)


# helper function that applies the double negation rule to a formula
#   the function removes all occurrences ~~ from the formula
def double_neg(formula):
    return formula.replace((neg+neg), '')


# Function that performs Depth First Search on a directed graph
# O(|V|+|E|)
def DFS(dir_graph, visited, stack, scc):
    for node in dir_graph.nodes:
        if node not in visited:
            explore(dir_graph, visited, node, stack, scc)


# DFS helper function that 'explores' as far as possible from a node
def explore(dir_graph, visited, node, stack, scc):
    if node not in visited:
        visited.append(node)
        for neighbour in dir_graph.graph[node]:
            explore(dir_graph, visited, neighbour, stack, scc)
        stack.append(node)
        scc.append(node)
    return visited


# Function that generates the transpose of a given directed graph
# Performance O(|V|+|E|)
def transpose_graph(d_graph):
    t_graph = dir_graph()
    # for each node in graph
    for node in d_graph.graph:
        # for each neighbour node of a single node
        for neighbour in d_graph.graph[node]:
            t_graph.addEdge(neighbour, node)
    return t_graph


# Function that finds all the strongly connected components in a given graph
# Implementation of Kosaraju’s algorithm
# Performance O(|V|+|E|) for a directed graph G=(V,E)
# IN : directed graph, G
# OUT: list of lists containing the strongly connected components of G
def strongly_connected_components(dir_graph):
    stack = []
    sccs = []
    DFS(dir_graph, [], stack, [])
    t_g = transpose_graph(dir_graph)
    visited = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc = []
            scc.append(node)
            explore(t_g, visited, node, [], scc)
            sccs.append(scc)
    return sccs


# Function that finds a contradiction in a list of strong connected components
# if [a , b , ~a,  c, a] is a connected component then the function returns T
# since a -> ~a -> a exists
# sccs = Strongly Connected Components
#   It is a list of lists representing the connected components
def find_contradiction(sccs):
    for component in sccs:
        for literal in component:
            for other_literal in component[component.index(literal):]:
                if other_literal == double_neg(neg + literal):
                    return True
    return False


# Function that determines if a given 2-CNF is Satisfiable or not
# Note: Modified slightly to return 'yes' or 'no' and to not print() anything
def two_sat_solver(two_cnf_formula):
    # setup the edges of the graph
    # G = (V,E) , V = L U ~L where L = set of variables in 2-CNF
    # E = {(~u,v),(~v,u) | for all clauses [u,v] } U {(~u,u) | for all clauses [u]}
    graph = dir_graph()
    for clause in two_cnf_formula.con:
        if len(clause) == 2:
            u = clause[0]
            v = clause[1]
            graph.addEdge(double_neg(neg+u), v)
            graph.addEdge(double_neg(neg+v), u)
        else:
            graph.addEdge(double_neg(neg+clause[0]), clause[0])
    if not find_contradiction(strongly_connected_components(graph)):
        return 'yes'
    else:
        return 'no'


def CNF_SAT_Solver(n, m, initial_states, connections): # O(m) + O(two_sat_solver)
    # Initialize a 2-CNF formula
    two_cnf_formula = two_cnf() # O(1)

    # Find and store the two switches controlling each light: O(m)
    lights = [[None, None] for i in range(m)] # O(m)
    for switch_idx, connection in enumerate(connections): # Outer loop: O(n)
        for light in connection: # Inner loop: average of O(m/n)
            if lights[light-1][0] == None:
                lights[light-1][0] = switch_idx
            else:
                lights[light-1][1] = switch_idx

    # Add a clause to the 2-CNF formula for each light depending on its initial state: O(m)
    for light_idx, light in enumerate(lights):
        if initial_states[light_idx] == 0:      # If light is initially off
            # Add condition that both or neither attached switch changes position
            two_cnf_formula.add_clause([f's{light[0]}', f'~s{light[1]}']) # O(1)
            two_cnf_formula.add_clause([f'~s{light[0]}', f's{light[1]}']) # O(1)
        else:                                   # If light is initially on
            # Add condition that exactly one attached switch changes position
            two_cnf_formula.add_clause([f's{light[0]}', f's{light[1]}']) # O(1)
            two_cnf_formula.add_clause([f'~s{light[0]}', f'~s{light[1]}']) # O(1)

    # Pass 2-CNF formula to 2-SAT solver and return the result
    return two_sat_solver(two_cnf_formula)


def can_turn_off_lights(input_file_path, output_file_path):
    # Read the input file
    instances = []
    with open(input_file_path, 'r') as file:
        content = file.read().strip()
        instance_strs = [instance_str for instance_str in content.split('***') if instance_str.strip()]

        for instance_str in instance_strs:
            instance_lines = instance_str.strip().split('\n')
            n, m = map(int, instance_lines[0].strip().split(','))
            initial_states = list(map(int, instance_lines[1].strip().split(',')))
            connections = [list(map(int, line.strip().split(','))) for line in instance_lines[2:]]
            instances.append((n, m, initial_states, connections))

    # Process the input
    results = [CNF_SAT_Solver(n, m, initial_states, connections) for n, m, initial_states, connections in instances]

    # Write to the output file
    with open(output_file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')
