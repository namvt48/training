from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        self.edges.append((u, v, w))

    def bellman_ford(self, src):
        distance = [float('inf')] * self.V
        predecessor = [-1] * self.V
        distance[src] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.edges:
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u

        affected_nodes = set()
        for u, v, w in self.edges:
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u
                affected_nodes.add(v)
                affected_nodes.add(u)

        return distance, predecessor, affected_nodes

    def find_negative_cycles(self):
        _, _, affected_nodes = self.bellman_ford(0)

        print(affected_nodes)

        # Data structures for DFS
        visited = [False] * self.V
        recursion_stack = [False] * self.V
        all_cycles = set()

        # Build adjacency list
        adj = defaultdict(list)
        for u, v, w in self.edges:
            adj[u].append((v, w))

        print(adj)

        # DFS function to find cycles
        def dfs(u, path):
            visited[u] = True
            recursion_stack[u] = True
            path.append(u)

            for v, w in adj[u]:
                if recursion_stack[v]:
                    # Found a cycle
                    cycle_start_index = path.index(v)
                    cycle = path[cycle_start_index:] + [v]
                    cycle_weight = sum(
                        self.get_edge_weight(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)
                    )
                    if cycle_weight < 0:
                        # Convert cycle to a tuple and store it with its weight
                        cycle_tuple = tuple(cycle)
                        all_cycles.add((cycle_tuple, cycle_weight))
                elif not visited[v]:
                    dfs(v, path)

            # Backtrack
            path.pop()
            recursion_stack[u] = False

        # Run DFS from affected nodes
        for node in affected_nodes:
            visited = [False] * self.V
            recursion_stack = [False] * self.V
            dfs(node, [])

        return all_cycles

    def get_edge_weight(self, u, v):
        """Returns the weight of the edge from u to v."""
        for edge in self.edges:
            if edge[0] == u and edge[1] == v:
                return edge[2]
        return 0  # Should not happen if the edge exists

# Example usage
if __name__ == "__main__":
    # Create a graph instance
    g = Graph(7)
    # Add edges (u, v, w)
    g.add_edge(0, 1, -3)
    g.add_edge(1, 2, -4)
    g.add_edge(2, 0, 1)
    g.add_edge(0, 3, -1)
    g.add_edge(3, 2, -2)
    g.add_edge(0, 4, 1)
    g.add_edge(4, 5, 1)
    g.add_edge(5, 6, 1)
    g.add_edge(6,0,1)

    # Find negative cycles
    negative_cycles = g.find_negative_cycles()

    # Print the negative cycles with their total weights
    print("Negative cycles found:")
    for cycle, weight in negative_cycles:
        cycle_str = " -> ".join(map(str, cycle))
        print(f"Cycle: {cycle_str}, Total Weight: {weight}")
