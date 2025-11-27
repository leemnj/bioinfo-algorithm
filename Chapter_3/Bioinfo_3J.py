# BA3J: Reconstruct a String from its Paired Composition
from textwrap import dedent

def build_paired_DBG(paired_reads):
    graph = {}
    for read in paired_reads:
        part1, part2 = read.split("|")
        prefix = part1[:-1] + "|" + part2[:-1]
        suffix = part1[1:] + "|" + part2[1:]
        graph.setdefault(prefix, []).append(suffix)
        
        if suffix not in graph:
            graph[suffix] = []
    return graph

def reconstruct_string_from_paired_DBG(graph, k, d):
    start = None
    for node in graph:
        out_degree = len(graph[node])
        in_degree = sum([1 for targets in graph.values() for target in targets if target == node])
        if out_degree > in_degree:
            start = node
            break
    if start is None:
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
            
    cycle = cycle[::-1]

    prefix_string = cycle[0].split("|")[0]
    suffix_string = cycle[0].split("|")[1]

    for node in cycle[1:]:
        prefix_string += node.split("|")[0][-1]
        suffix_string += node.split("|")[1][-1]

    return prefix_string + suffix_string[-(k + d):]


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3j.txt") as f:
            data = f.read().strip().splitlines()
    except:
        data = dedent("""4 2
                GAGA|TTGA
                TCGT|GATG
                CGTG|ATGT
                TGGT|TGAG
                GTGA|TGTT
                GTGG|GTGA
                TGAG|GTTG
                GGTC|GAGA
                GTCG|AGAT""").strip().splitlines()
    k, d = map(int, data[0].split())
    paired_reads = [line.strip() for line in data[1:]]
    pairedDBG = build_paired_DBG(paired_reads)
    result = reconstruct_string_from_paired_DBG(pairedDBG, k, d)
    print(result)
    with open("output/3J.txt", "w") as f:
        f.write(result)