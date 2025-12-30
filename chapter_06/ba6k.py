# BA6K: 2-BreakOnGenome
# BA6K: Implement 2-BreakOnGenome (3-function version)

def read_input(line1: str, line2: str):
    # genome 파싱: "(+1 -2 -4 +3)(+5 -6)" -> [[1,-2,-4,3],[5,-6]]
    genome = []
    s = line1.strip()
    i, n = 0, len(s)
    while i < n:
        if s[i] == '(':
            i += 1
            chrom, token = [], ""
            while i < n and s[i] != ')':
                if s[i] == ' ':
                    if token:
                        chrom.append(int(token))
                        token = ""
                else:
                    token += s[i]
                i += 1
            if token:
                chrom.append(int(token))
            genome.append(chrom)
        i += 1

    # indices 파싱: "1, 6, 3, 8" -> [1,6,3,8]
    idx = list(map(int, line2.replace(" ", "").split(",")))
    return genome, idx[0], idx[1], idx[2], idx[3]


def do_2break_and_return_graph(P, a, b, c, d):
    # ChromosomeToCycle
    def chr_to_cycle(chrom):
        nodes = []
        for x in chrom:
            if x > 0:
                nodes += [2 * x - 1, 2 * x]
            else:
                x = -x
                nodes += [2 * x, 2 * x - 1]
        return nodes

    # ColoredEdges(P)
    edges = []
    for chrom in P:
        nodes = chr_to_cycle(chrom)
        m = len(chrom)
        for j in range(m):
            edges.append((nodes[2 * j + 1], nodes[(2 * j + 2) % (2 * m)]))

    # 2-BreakOnGenomeGraph: remove (a,b),(c,d) add (a,c),(b,d)
    def norm(x, y):
        return (x, y) if x < y else (y, x)

    S = {norm(x, y) for x, y in edges}
    S.discard(norm(a, b))
    S.discard(norm(c, d))
    S.add(norm(a, c))
    S.add(norm(b, d))

    return list(S)  # genome graph의 colored edges (edge list)


def graph_to_genome(graph_edges):
    def black_pair(x: int) -> int:
        return x + 1 if x % 2 == 1 else x - 1

    # colored neighbor map
    colored = {}
    for x, y in graph_edges:
        colored[x] = y
        colored[y] = x

    genome = []
    used = set()

    for start in colored:
        if start in used:
            continue

        # cycle 만들기: colored -> black 반복
        cycle = []
        v = start
        while True:
            v = colored[v]
            cycle.append(v)
            used.add(v)

            v = black_pair(v)
            cycle.append(v)
            used.add(v)

            if v == start:
                break

        # CycleToChromosome
        chrom = []
        for i in range(0, len(cycle), 2):
            x, y = cycle[i], cycle[i + 1]
            if x < y:
                chrom.append(y // 2)
            else:
                chrom.append(-(x // 2))

        genome.append(chrom)

    return genome


if __name__ == "__main__":
    try:
        with open("inpㅏut/rosalind_ba6k.txt", "r") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
    except:
        line1 = "(+1 -2 -4 +3)"
        line2 = "1, 6, 3, 8"

    P, a, b, c, d = read_input(line1, line2)
    G = do_2break_and_return_graph(P, a, b, c, d)
    P2 = graph_to_genome(G)

    print("".join("(" + " ".join(f"{x:+d}" for x in chrom) + ")" for chrom in P2))
