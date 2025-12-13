# BA6G: CycletoChromosome
def parse_nodes(line: str):
    # "(1 2 4 3 6 5 7 8)" -> [1,2,4,3,6,5,7,8]
    line = line.strip()
    line = line[1:-1]  # remove parentheses
    return list(map(int, line.split()))

def cycle_to_chromosome(nodes):
    chrom = []
    for j in range(0, len(nodes), 2):
        a = nodes[j]
        b = nodes[j + 1]
        if a < b:
            chrom.append(b // 2)
        else:
            chrom.append(-(a // 2))
    return chrom

def main():
    try:
        with open("input/rosalind_ba6g.txt", "r") as f:
            line = f.readline().strip()
    except:
        line = "(1 2 4 3 6 5 7 8)"
    nodes = parse_nodes(line)
    chrom = cycle_to_chromosome(nodes)
    print("(" + " ".join(f"{x:+d}" for x in chrom) + ")")

if __name__ == "__main__":
    main()
