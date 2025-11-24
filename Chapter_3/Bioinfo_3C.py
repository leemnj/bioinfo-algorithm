# BA3C: Construct the Overlap Graph of a Collection of k-mers

def build_overlap_graph(kmers):
    prefix_map = {}
    overlap_graph = []
    for kmer in kmers:
        prefix = kmer[:-1]
        prefix_map.setdefault(prefix, []).append(kmer)

    for kmer in sorted(kmers):
        suffix = kmer[1:]
        if suffix in prefix_map:
            for neighbor in prefix_map[suffix]:
                overlap_graph.append((kmer, neighbor))
    return overlap_graph

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba3c.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = """ATGCG
GCATG
CATGC
AGGCA
GGCAT""".splitlines()
    result = build_overlap_graph(data)
    for edge in result:
        print(f"{edge[0]} -> {edge[1]}")