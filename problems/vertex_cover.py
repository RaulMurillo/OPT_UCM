from problem import Problem
import numpy as np
import itertools
import csv
import sys


class Vertex_Cover(Problem):
    def __init__(self, N, data):
        super().__init__()
        # self.solver = solvers_dict[solver.lower()]()
        self.P = {"N": N}
        self.data = data
        # data[:,0] is number of elements in set
        print()
        print("="*10+" The Vertex Cover Problem "+"="*10)
        print("* Number of vertex:", N)
        # print("* DATA:", self.data) # Caution when using large data
        print('-'*42)
        print()
    
    def resolve(self, method):
        print("Solving Set cover Problem using " + method + " algorithm")
        best_sets = super().resolve(method)
        if len(best_sets):
            print("Best solution takes vertices:")
            # best_sets.sort()
            print(best_sets)
        print()

    def GreedyAlg(self):
        graph = self.data.copy()
        vertices = []
        while(graph): # while uncovered graph is not empty
            # print('*'*10)
            # print(graph)
            # pick/remove any node in graph (last one)
            v1, edges = graph.popitem()
            if(edges): # node v1 is not isolated
                v2 = edges[0]
                # remove this node from graph
                graph.pop(v2)
                vertices.append((v1, v2))
            else: # node v1 is isolated - not useful
                continue

            # remove edges from graph
            for n, e in graph.items():
                if v1 in e:
                    graph[n].remove(v1)
                if v2 in e:
                    graph[n].remove(v2)
            
        
        return vertices



def read_file(fname):
    with open(fname, 'r', newline='') as csv_file:
        data = list(csv.reader(csv_file, delimiter=' '))

    # Convert to int
    data = [[int(j) for j in i] for i in data]
    return data

def read_graph(N, data):
    graph = {}
    ch = 'A'
    # chr(ord(ch) + 1)
    for i in range(N):
        graph[chr(ord(ch) + i)] = []

    for i in range(1, N):
        edges = data[i-1]
        for j, edge in enumerate(edges):
            if edge:
                graph[chr(ord(ch) + i)].append(chr(ord(ch) + j))
                graph[chr(ord(ch) + j)].append(chr(ord(ch) + i))

    return graph



if __name__ == "__main__":
    # import numpy as np
    import time


    my_data = read_file('data/graph.txt')
    N = int(my_data[0][0])
    graph = read_graph(N, my_data[1:])

    my_VertexCover = Vertex_Cover(N, graph)
    
    tic = time.time()
    my_VertexCover.resolve('greedy') # Choose between exhaustive, greedy, dynamic, fptas
    toc = time.time()
    print('Elapsed time:', toc-tic)
    print('-'*42 + '\n')
    
    # tic = time.time()
    # my_SetCover.resolve('exhaustive') # Choose between exhaustive, greedy, dynamic, fptas
    # toc = time.time()
    # print('Elapsed time:', toc-tic)
    # print('-'*42 + '\n')