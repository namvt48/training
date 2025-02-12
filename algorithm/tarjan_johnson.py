

class Graph:
    def __init__(self, num_vertices):
        self.V = list(range(num_vertices))
        self.graph = [[] for _ in range(num_vertices)]
        self.edges = [{} for _ in range(num_vertices)]
    def add_edge(self, u, v, weight):
        self.graph[u].append(v)
        self.edges[u][v] = weight

    def tarjan_scc(self):
        index = 0
        indices = [None] * len(self.V)
        lowlink = [None] * len(self.V)
        on_stack = [False] * len(self.V)
        S = []
        SCCs = []

        def strongconnect(v):
            nonlocal index
            indices[v] = index
            lowlink[v] = index
            index += 1
            S.append(v)
            on_stack[v] = True

            for w in self.graph[v]:
                if indices[w] is None:
                    strongconnect(w)
                    lowlink[v] = min(lowlink[v], lowlink[w])
                elif on_stack[w]:
                    lowlink[v] = min(lowlink[v], indices[w])

            if lowlink[v] == indices[v]:
                # Start a new SCC
                scc = []
                while True:
                    w = S.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == v:
                        break
                SCCs.append(scc)

        for v in self.V:
            if indices[v] is None:
                strongconnect(v)

        return SCCs

    def johnson_algorithm(self):

        self.blocked = set()
        self.B = [set() for _ in range(len(self.V))]
        self.stack = []
        self.cycles = []

        def circuit(v, s):
            f = False
            self.stack.append(v)
            self.blocked.add(v)
            for w in self.graph[v]:
                if w == s:
                    self.cycles.append(self.stack.copy())
                    f = True
                elif w not in self.blocked:
                    if circuit(w, s):
                        f = True
            if f:
                self.unblock(v)
            else:
                for w in self.graph[v]:
                    self.B[w].add(v)
            self.stack.pop()
            return f

        def circuits_in_scc(scc):
            subgraph_nodes = sorted(scc)
            self.blocked = set()
            self.B = [set() for _ in range(len(self.V))]
            self.stack = []
            for s in subgraph_nodes:
                self.blocked = set()
                self.B = [set() for _ in range(len(self.V))]
                circuit(s, s)

        self.cycles = []
        SCCs = self.tarjan_scc()
        for scc in SCCs:
            if len(scc) > 1 or (len(scc) == 1 and scc[0] in self.graph[scc[0]]):
                circuits_in_scc(scc)

        return self.cycles

    def unblock(self, u):
        self.blocked.discard(u)
        while self.B[u]:
            w = self.B[u].pop()
            if w in self.blocked:
                self.unblock(w)

    def find_negative_cycles(self):

        cycles = self.johnson_algorithm()
        negative_cycles = []
        unique_cycles = set()
        for cycle in cycles:
            weight = 0
            cycle_edges = []
            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                weight += self.edges[u][v]
                cycle_edges.append((u, v))
            min_index = cycle.index(min(cycle))
            canonical_cycle = tuple(cycle[min_index:] + cycle[:min_index])
            if weight < 0 and canonical_cycle not in unique_cycles:
                unique_cycles.add(canonical_cycle)
                negative_cycles.append((cycle, weight))
        return negative_cycles

# Example usage:
g = Graph(4)
# Add edges (u, v, w)
g.add_edge(0, 1, -3)
g.add_edge(1, 2, -4)
g.add_edge(2, 0, 1)
g.add_edge(0, 3, -1)
g.add_edge(3, 2, -2)


# Find all negative cycles
negative_cycles = g.find_negative_cycles()

# Print the negative cycles
print("Negative Cycles:")
for cycle, weight in negative_cycles:
    cycle_str = " -> ".join(map(str, cycle + [cycle[0]]))
    print(f"Cycle: {cycle_str}, Weight: {weight}")
