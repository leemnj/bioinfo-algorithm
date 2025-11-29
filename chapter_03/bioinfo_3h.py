# BA3H: Reconstructing a String from its k-mer Composition
from textwrap import dedent

def reconstruct_string_from_kmers(kmers):
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
    for node in graph:
        if prefix_count[node] > suffix_count[node]:
            start = node
            break

    # Eulerian cycle case: use any node as start
    if start is None:
        start = next(iter(graph))

    stack = [start]
    path = []
    local = {k: v[:] for k, v in graph.items()}

    while stack:
        node = stack[-1]
        if local[node]:
            nxt = local[node].pop(0)
            stack.append(nxt)
        else:
            path.append(stack.pop())

    path = path[::-1]

    text = path[0]
    for node in path[1:]:
        text += node[-1]

    return text


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3h.txt") as f:
            data = f.read().strip().splitlines()
    except:
        data = dedent("""
            4
            CTTA
            ACCA
            TACC
            GGCT
            GCTT
            TTAC""").strip().splitlines()
    kmers = data[1:]
    
    result = reconstruct_string_from_kmers(kmers)
    print(result)
    
    with open("output/3H.txt", "w") as f:
        f.write(result)