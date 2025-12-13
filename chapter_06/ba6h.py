# BA6H: Implement ColoredEdges

def parse_genome(line: str):
    line = line.strip()
    genome = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] == '(':
            i += 1
            buf = []
            token = ""

            while i < n and line[i] != ')':
                ch = line[i]
                if ch == ' ':
                    if token:
                        buf.append(int(token))
                        token = ""
                else:
                    token += ch
                i += 1

            if token:
                buf.append(int(token))
            genome.append(buf)  # 한 chromosome 완료

        i += 1

    return genome


def chromosome_to_cycle(chrom):
    """
    +i -> (2i-1, 2i)
    -i -> (2i, 2i-1)
    """
    nodes = []
    for x in chrom:
        if x > 0:
            nodes.append(2 * x - 1)
            nodes.append(2 * x)
        else:
            x = -x
            nodes.append(2 * x)
            nodes.append(2 * x - 1)
    return nodes


def colored_edges(P):
    edges = []
    for chrom in P:
        nodes = chromosome_to_cycle(chrom)
        m = len(chrom)
        for j in range(m):
            a = nodes[2 * j + 1]
            b = nodes[(2 * j + 2) % (2 * m)]
            edges.append((a, b))
    return edges


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba6h.txt", "r") as f:
            line = f.readline().strip()
    except:
        line = "(+1 -2 -3)(+4 +5 -6)"

    P = parse_genome(line)
    edges = colored_edges(P)

    print(", ".join(f"({a}, {b})" for a, b in edges))
