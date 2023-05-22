# from itertools import combinations

# def held_karp(dists):
#     n = len(dists)

#     C = {}
#     for k in range(1, n):
#         C[(1 << k, k)] = (dists[0][k], 0)

#     for _ in range(2, n):
#         for subset in combinations(range(1, n), _):
#             bits = 0
#             for bit in subset:
#                 bits |= 1 << bit

#             for k in subset:
#                 prev = bits & ~(1 << k)
#                 res = []
#                 for m in subset:
#                     if m == 0 or m == k:
#                         continue
#                     res.append((C[(prev, m)][0] + dists[m][k], m))
#                 C[(bits, k)] = min(res)

#     bits = (2**n - 1) - 1

#     return min((C[(bits, k)][0] + dists[k][0], k) for k in range(1, n))

# # Define the distance matrix for a 5-city problem
# dists = [
#     [0, 20, 30, 10, 11],
#     [15, 0, 16, 4, 2],
#     [3, 5, 0, 2, 4],
#     [19, 6, 18, 0, 3],
#     [16, 4, 7, 16, 0]
# ]

# # Run the Held-Karp algorithm
# result = held_karp(dists)

# # Print the result
# print(f"The shortest cycle length is {result[0]} and ends at city {result[1] + 1}")

import tsplib95
import networkx as nx
from itertools import combinations

def held_karp(G):
    n = G.number_of_nodes()
    C = {}
    
    # Initialization
    for k in range(1, n):
        C[(1 << k, k)] = (G[0][k]['weight'], 0)
    
    # Loops for all subsets of vertices
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            
            # Find the shortest path to every vertex
            for k in subset:
                prev = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + G[m][k]['weight'], m))
                C[(bits, k)] = min(res)
    
    # Connect to the starting point
    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + G[k][0]['weight'], k))
    
    opt, parent = min(res)

    # Unravel the path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0)
    
    return opt, list(reversed(path))

# Load TSP data from a file
problem = tsplib95.load('berlin52.tsp')
G = problem.get_graph()

opt, path = held_karp(G)
print('Optimal cost:', opt)
print('Optimal path:', ' -> '.join(map(str, path)))
