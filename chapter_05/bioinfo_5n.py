# Topological Sort
# 5D 참고
from collections import defaultdict
try:
    with open("inputs/rosalind_ba5n.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''1 -> 2
2 -> 3
4 -> 2
5 -> 3

'''

lines = content.split('\n')
edges = [line for line in lines if line.strip() != ""]

# u -> v
def topological_sort(edges):
    graph = defaultdict(list)
    indegree = {}
    nodes = set()

    for edge in edges:
        parts = edge.split('->') 
        u, targets = parts[0].strip(), parts[1].strip().split(',')
        if u not in graph:
            graph[u] = []
        indegree.setdefault(u, 0)
        nodes.add(u)

        for v in targets:
            v = v.strip()
            graph[u].append(v)
            indegree.setdefault(v, 0)
            indegree[v] += 1 
            nodes.add(v)

    queue = []
    for node in nodes:
        if indegree[node] == 0:
            queue.append(node)
    
    result = []

    while queue:
        curr = queue.pop()
        result.append(curr)

        neighbors = graph[curr]
        for neighbor in neighbors:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return result

print(*topological_sort(edges), sep = ", ")