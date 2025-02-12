import pandas as pd
import numpy as np
import networkx as nx
import math
from collections import defaultdict


def bellman_ford_negative_cycles(g, s):
    n = len(g.nodes())
    d = defaultdict(lambda: math.inf)  # distances dict
    p = defaultdict(lambda: -1)  # predecessor dict
    d[s] = 0

    for _ in range(n - 1):
        for u, v in g.edges():
            # Bellman-Ford relaxation
            weight = g[u][v]["weight"]
            if d[u] + weight < d[v]:
                d[v] = d[u] + weight
                p[v] = u  # update pred

    # Find cycles if they exist
    all_cycles = []
    seen = defaultdict(lambda: False)

    for u, v in g.edges():
        weight = g[u][v]["weight"]
        # If we can relax further, there must be a neg-weight cycle
        if seen[v]:
            continue

        if d[u] + weight < d[v]:
            cycle = []
            x = v
            while True:
                # Walk back along predecessors until a cycle is found
                seen[x] = True
                cycle.append(x)
                x = p[x]
                if x == v or x in cycle:
                    break
            # Slice to get the cyclic portion
            idx = cycle.index(x)
            cycle.append(x)
            all_cycles.append(cycle[idx:][::-1])
    return all_cycles


def all_negative_cycles(g):
    all_paths = []
    for v in g.nodes():
        all_paths.append(bellman_ford_negative_cycles(g, v))
    flatten = lambda l: [item for sublist in l for item in sublist]
    return [list(i) for i in set(tuple(j) for j in flatten(all_paths))]


def calculate_arb(cycle, g, verbose=True):
    total = 0
    for (p1, p2) in zip(cycle, cycle[1:]):
        total += g[p1][p2]["weight"]
    arb = np.exp(-total) - 1
    if verbose:
        print("Path:", cycle)
        print(f"{arb*100:.2g}%\n")
    return arb


def find_arbitrage(filename="snapshot.csv", find_all=False, sources=None):
    df = pd.read_csv(filename, header=0, index_col=0)
    g = nx.DiGraph(-np.log(df).fillna(0).T)

    if nx.negative_edge_cycle(g):
        print("ARBITRAGE FOUND\n" + "=" * 15 + "\n")

        if find_all:
            unique_cycles = all_negative_cycles(g)
        else:
            all_paths = []
            for s in sources:
                all_paths.append(bellman_ford_negative_cycles(g, s))
            flatten = lambda l: [item for sublist in l for item in sublist]
            unique_cycles = [list(i) for i in set(tuple(j) for j in flatten(all_paths))]

        for p in unique_cycles:
            calculate_arb(p, g)
        return unique_cycles

    else:
        print("No arbitrage opportunities")
        return None


if __name__ == "__main__":
    find_arbitrage(find_all=True)