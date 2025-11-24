# BA3D: Construct the De Bruijn Graph of a Collection of k-mers

def build_de_bruijn_graph(string):
    de_bruijn_graph = {}
    kmers = [string[i:i+k] for i in range(len(string) - k + 1)]

    for kmer in sorted(kmers):
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in de_bruijn_graph:
            de_bruijn_graph[prefix] = []
        de_bruijn_graph[prefix].append(suffix)
    return de_bruijn_graph

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3d.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = """4
AAGATTCTCTAC
""".splitlines()
    k = int(data[0])
    string = data[1]
    result = build_de_bruijn_graph(string)
    for prefix in sorted(result.keys()):
        print(f"{prefix} -> {', '.join(result[prefix])}")
    with open("output/3D.txt", "w") as f:
        for prefix in sorted(result.keys()):
            f.write(f"{prefix} -> {', '.join(result[prefix])}\n")