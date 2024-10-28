from typing import List, Tuple


def bellman_ford(graph: List[Tuple[str, str, float]], source: str) -> Tuple[dict[str, int], List[str] | None]:
    distances = {}
    distances[source] = 0

    pre = {}

    for u, v, w in graph:
        distances[u] = 0
        distances[v] = 0
        pre[u] = None
        pre[v] = None

    num_vertices = len(distances)

    for _ in range(num_vertices - 1):
        for u, v, w in graph:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                pre[v] = u

    for u, v, w in graph:
        if distances[u] + w < distances[v]:

            negative_cycle = []
            visited = set()

            x = v
            for _ in range(num_vertices):
                x = pre[x]

            start = x

            while True:
                if x in visited:
                    break
                visited.add(x)
                negative_cycle.append(x)
                x = pre[x]

            negative_cycle.append(start)
            negative_cycle.reverse()
            return distances, negative_cycle

    return distances, None


# Ví dụ sử dụng
if __name__ == "__main__":
    graph = [
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('C', 'D', 2),
        ('D', 'B', -6),
    ]

    distances, negative_cycle = bellman_ford(graph, 'A')

    if negative_cycle:
        print("Negative cycle:")
        for item in negative_cycle:
            print(item)
    else:
        print("Distances from root:")
        for vertex in distances:
            print(f"{vertex}: {distances[vertex]}")
