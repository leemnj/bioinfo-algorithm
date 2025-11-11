try:
    with open("Chapter_5/rosalind_ba5d.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''0
4
0->1:7
0->2:4
2->3:2
1->4:1
3->4:3'''

lines = content.split('\n')

start, end = lines[0], lines[1]
edges = lines[2:] # 끝에 공백으로 처리되는 걸 어떻게 처리할지

graph = {}
indegree = {}
nodes = set()

# 1. making graph

for edge in edges:
    # u->v:w
    u, rest = edge.split('->')
    v, w = rest.split(':')
    w = int(w)

    nodes.add(u)
    nodes.add(v)

    if u not in graph:
        graph[u] = []
    graph[u].append((v, w))

    indegree.setdefault(u, 0)
    indegree.setdefault(v, 0)
    indegree[v] += 1

# 2. topological sort
queue = [n for n in nodes if indegree.get(n, 0)==0]
topo_order = []

while queue:
    u = queue.pop(0)
    topo_order.append(u)

    for v, w in graph.get(u, []):
        indegree[v] -= 1
        if indegree[v]==0:
            queue.append(v)

# 3. initialize DP
dist = {node: -float('inf') for node in nodes}
parent = {node: None for node in nodes}
dist[start] = 0

# 4. relaxation
for u in topo_order:
    if dist[u] == -float('inf'):
        continue

    for v, w in graph.get(u, []):
        if dist[v] < dist[u] + w:
            dist[v] = dist[u] + w
            parent[v] = u

# 5. print output & restore path
longest_length = dist[end]
path = []
curr = end
while curr is not None:
    path.append(curr)
    if curr == start:
        break
    curr = parent.get(curr)
path.reverse()

print(longest_length)
print("->".join(path))