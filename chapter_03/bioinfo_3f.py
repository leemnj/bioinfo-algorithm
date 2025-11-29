# BA3F: Eulerian Cycle in a Graph

def MakeGraph(lines):
    graph = {}
    for line in lines:
        node, targets = line.strip().split(" -> ")
        graph[node] = targets.split(",")
    return graph


def EulerianCycle(graph):
    
    start = next(iter(graph))

    stack = [start]
    cycle = []

    while stack:
        node = stack[-1]
        if graph[node]: # graph[node] is not empty
            next_node = graph[node].pop(0)
            stack.append(next_node)
        else: # graph[node] is empty
            cycle.append(stack.pop())
            
    return cycle[::-1]


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3f.txt", "r") as f:
            input_data = f.read().strip().splitlines()
    except:
        input_data = """0 -> 3
1 -> 0
2 -> 1,6
3 -> 2
4 -> 2
5 -> 4
6 -> 5,8
7 -> 9
8 -> 7
9 -> 6""".strip().splitlines()

    graph = MakeGraph(input_data)
    result = EulerianCycle(graph)

    with open("output/3F.txt", "w") as f:
        f.write("->".join(result))