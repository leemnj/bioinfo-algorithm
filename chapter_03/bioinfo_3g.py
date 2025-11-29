# BA3G: Eulerian Path in a Graph
'''
3F는 indegree = outdegree
3G는 indegree, outdegree 차이가 1인 노드가 2개 존재

근데 cycle이면 모든 노드가 indegree = outdegree
'''
from textwrap import dedent

def build_graph(lines):
    graph = {}
    indegree = {}
    outdegree = {}

    for line in lines:
        node, out = line.strip().split(" -> ")
        targets = out.split(",")
        graph[node] = targets
        outdegree[node] = len(targets)
        for t in targets:
            indegree[t] = indegree.get(t, 0) + 1
            if t not in graph:
                graph[t] = []

    for node in graph:
        indegree[node] = indegree.get(node, 0)
        outdegree[node] = outdegree.get(node, 0)

    start = end = None

    for node in graph:
        if outdegree[node] == indegree[node] + 1:
            start = node
        elif indegree[node] == outdegree[node] + 1:
            end = node

    # 🔥 Cycle인 경우 (=end 없음)
    if start is None and end is None:
        start = end = next(iter(graph))
    elif end is None:  # path지만 end 못 찾은 경우 fallback
        end = start

    return graph, start, end



def eulerian_path(graph, start, end):
    
    graph = {k: v[:] for k, v in graph.items()}

    # add virtual edge
    graph[end].append(start)
    
    stack = [end]
    cycle = []

    while stack:
        node = stack[-1]
        if graph[node]:
            nxt = graph[node].pop(0)
            stack.append(nxt)
        else:
            cycle.append(stack.pop())

    cycle = cycle[::-1]

    # remove virtual edge
    for i in range(len(cycle) - 1):
        if cycle[i] == end and cycle[i+1] == start:
            path = cycle[i+1:] + cycle[1:i+1]    # 잘라내기

    return path

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3g.txt", "r") as f:
            input_data = f.read().strip().splitlines()
    except:
        input_data = dedent("""
            0 -> 2
            1 -> 3
            2 -> 1
            3 -> 0,4
            6 -> 3,7
            7 -> 8
            8 -> 9
            9 -> 6
        """).strip().splitlines()
    
    result = eulerian_path(*build_graph(input_data))
    with open("output/3G.txt", "w") as f:
        f.write("->".join(result))
    print("->".join(result))