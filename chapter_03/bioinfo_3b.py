# BA3B: Reconstruct a String from its Genome Path

def StringReconstruction(kmers):
    prefix_map = {}
    suffix_map = {}
    
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        prefix_map.setdefault(prefix, []).append(suffix)
        suffix_map.setdefault(suffix, []).append(prefix)
    
    start_node = None

    for node in prefix_map:
        out_degree = len(prefix_map[node])
        in_degree = len(suffix_map.get(node, []))
        if out_degree - in_degree == 1:
            start_node = node
            break
    
    if not start_node:
        start_node = kmers[0][:-1]
    
    path = [start_node]
    while True:
        current_node = path[-1]
        if current_node in prefix_map and prefix_map[current_node]:
            next_node = prefix_map[current_node].pop()
            path.append(next_node)
        else:
            break
    
    reconstructed_string = path[0]
    for node in path[1:]:
        reconstructed_string += node[-1]
    
    return reconstructed_string

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba3b.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = """ACCGA
CCGAA
CGAAG
GAAGC
AAGCT""".splitlines()
    result = StringReconstruction(data)
    print(result)