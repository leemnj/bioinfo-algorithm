# BA3I: k-Universal Circular String
'''
circular string -> length = 2^k
'''
from itertools import product

def generate_all_kmers(k):
    return ["".join(p) for p in product("01", repeat=k)]


def k_universal_circular_string(kmers):
    graph = {}
    prefix_count = {}
    suffix_count = {}

    for kmer in kmers:
        prefix, suffix = kmer[:-1], kmer[1:]

        graph.setdefault(prefix, []).append(suffix)

        prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
        suffix_count[suffix] = suffix_count.get(suffix, 0) + 1

        if suffix not in graph:
            graph[suffix] = []

        prefix_count.setdefault(suffix, 0)
        suffix_count.setdefault(prefix, 0)

    start = None
    if start is None:
        start = next(iter(graph))  # cycle case

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
    
    text = cycle[0]
    for node in cycle[1:]:
        text += node[-1]
        
    return text[:2**k]


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3i.txt") as f:
            data = f.read().strip().splitlines()
            k = int(data[0])
    except:
        k=4
    kmers = generate_all_kmers(k)
    result = k_universal_circular_string(kmers)
    output = "".join(result)
    print(len(output))
    print(output)
    with open("output/3I.txt", "w") as f:
        f.write(output)