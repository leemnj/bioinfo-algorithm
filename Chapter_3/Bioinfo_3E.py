# BA3E: Construct the De Bruijn Graph of a Collection of k-mers

def build_de_bruijn_graph_from_kmers(kmers):
    de_bruijn_graph = {}
    
    for kmer in sorted(kmers):
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in de_bruijn_graph:
            de_bruijn_graph[prefix] = []
        de_bruijn_graph[prefix].append(suffix)
    
    return de_bruijn_graph

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3e.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = """GAGG
CAGG
GGGG
GGGA
CAGG
AGGG
GGAG
""".strip().splitlines()
        
    result = build_de_bruijn_graph_from_kmers(data)
with open("output/3E.txt", "w") as f:
    for prefix in sorted(result.keys()):
        f.write(f"{prefix} -> {', '.join(result[prefix])}\n")