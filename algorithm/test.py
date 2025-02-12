import sys
import threading

def simple_cycles(G):
    """
    Johnson's algorithm for finding all simple cycles in a directed graph.
    Yields cycles as lists of nodes.
    """
    index = {}
    stack = []
    blocked = set()
    B = {}
    cycles = []

    def circuit(v, s, adj):
        f = False
        stack.append(v)
        blocked.add(v)
        for w in adj[v]:
            if w == s:
                yield stack[:]
                f = True
            elif w not in blocked:
                for c in circuit(w, s, adj):
                    yield c
                    f = True
        if f:
            unblock(v)
        else:
            for w in adj[v]:
                B.setdefault(w, set()).add(v)
        stack.pop()
        return

    def unblock(u):
        blocked.discard(u)
        if u in B:
            for w in B[u]:
                if w in blocked:
                    unblock(w)
            del B[u]

    # Main algorithm
    sccs = strongly_connected_components(G)
    for scc in sccs:
        if len(scc) > 1:
            subgraph = {v: G[v] & scc for v in scc}
            start_node = min(scc)
            blocked = set()
            B = {}
            stack = []
            for cycle in circuit(start_node, start_node, subgraph):
                yield cycle
        elif scc:
            v = next(iter(scc))
            if v in G and v in G[v]:
                # Self-loop
                yield [v]

def strongly_connected_components(graph):
    """
    Tarjan's algorithm for finding strongly connected components.
    Returns a list of sets, each containing the nodes of a strongly connected component.
    """
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        try:
            successors = graph[node]
        except KeyError:
            successors = []
        for successor in successors:
            if successor not in index:
                # Successor has not yet been visited; recurse on it
                strongconnect(successor)
                lowlink[node] = min(lowlink[node], lowlink[successor])
            elif successor in stack:
                # Successor is in stack and hence in the current SCC
                lowlink[node] = min(lowlink[node], index[successor])

        # If node is a root node, pop the stack and output an SCC
        if lowlink[node] == index[node]:
            connected_component = set()
            while True:
                successor = stack.pop()
                connected_component.add(successor)
                if successor == node:
                    break
            result.append(connected_component)

    for node in graph:
        if node not in index:
            strongconnect(node)
    return result

def find_negative_cycles(G, edge_weights):
    """
    Find and print all negative cycles in the graph G with given edge weights.
    """
    cycles = []
    for cycle in simple_cycles(G):
        total_weight = 0
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            total_weight += edge_weights.get((u, v), float('inf'))
        if total_weight < 0:
            cycles.append((cycle, total_weight))

    # Print all negative cycles
    if cycles:
        print("Negative cycles found:")
        for cycle, weight in cycles:
            print(f"Cycle: {cycle} | Total Weight: {weight}")
    else:
        print("No negative cycles found.")

# Example usage
if __name__ == "__main__":
    # Increase recursion limit and stack size for large graphs
    sys.setrecursionlimit(1 << 25)
    threading.stack_size(1 << 27)

    # Define the graph as an adjacency list and edge weights
    G = {
        'A': {'B'},
        'B': {'C', 'E'},
        'C': {'A', 'D'},
        'D': {'E'},
        'E': {'D'}
    }

    edge_weights = {
        ('A', 'B'): 1,
        ('B', 'C'): 1,
        ('C', 'A'): -3,  # Negative weight edge creating a negative cycle
        ('B', 'E'): 2,
        ('C', 'D'): 1,
        ('D', 'E'): -1,
        ('E', 'D'): -1,  # Negative weight edge creating another negative cycle
    }

    # Run the function to find and print all negative cycles
    def main():
        find_negative_cycles(G, edge_weights)

    # Run in a separate thread to handle increased stack size
    threading.Thread(target=main).start()
