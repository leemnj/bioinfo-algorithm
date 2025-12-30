# BA7A: Distance b.w/ Leaves
import sys
from collections import defaultdict, deque

def parse_edge(line: str):
    # format: "u->v:w"
    left, w_str = line.strip().split(":")
    u_str, v_str = left.split("->")
    return int(u_str), int(v_str), int(w_str)

def distances_from(start, graph):
    dist = {}
    dist[start] = 0
    stack = [start]

    while stack:
        u = stack.pop()
        for v, w in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + w
                stack.append(v)
    return dist

def main():
    try:
        with open("input/rosalind_ba7a.txt", "r") as f:
            data = f.read().strip().split('\n')
            n, data = int(data[0]), data[1:]
    except:
        # sample input
        n = 4
        data = \
'''0->4:11
1->4:2
2->5:6
3->5:7
4->0:11
4->1:2
4->5:4
5->4:4
5->3:7
5->2:6'''.strip().split('\n')

    graph = defaultdict(list)

    for line in data:
        u, v, w = parse_edge(line)
        graph[u].append((v, w))

    out_lines = []
    for i in range(n):
        dist = distances_from(i, graph)
        row = [str(dist[j]) for j in range(n)]
        out_lines.append("\t".join(row))

    print("\n".join(out_lines))

    with open("output/ba7a.txt", "w") as f:
        f.write("\n".join(out_lines))
if __name__ == "__main__":
    main()
