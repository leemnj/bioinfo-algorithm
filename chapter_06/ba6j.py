# BA6J: Implement 2-BreakOnGenomeGraph
# 6d 참고

def parse_edges(line: str):
    nums, cur = [], ""
    for ch in line:
        if ch.isdigit():
            cur += ch
        else:
            if cur:
                nums.append(int(cur))
                cur = ""
    if cur:
        nums.append(int(cur))
    return [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]


def parse_indices(line: str):
    return list(map(int, line.replace(" ", "").split(",")))


def two_break_on_genome_graph(edges, u, v, x, y):
    """
    edges: dict (node -> neighbor)
    remove (u,x), (v,y)
    add (u,v), (x,y)
    """
    # 기존 연결 삭제
    del edges[u]; del edges[x]
    del edges[v]; del edges[y]

    # 새로운 연결 추가
    edges[u] = x; edges[v] = y
    # edges[x] = u; edges[y] = v


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba6j.txt") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
    except:
        line1 = "(2, 4), (3, 8), (7, 5), (6, 1)"
        line2 = "1, 6, 3, 8"

    edge_list = parse_edges(line1)
    u, v, x, y = parse_indices(line2)

    # list → dict
    edges = {}
    for a, b in edge_list:
        edges[a] = b
        edges[b] = a

    two_break_on_genome_graph(edges, u, v, x, y)

    # dict → list (중복 없이)
    used = set()
    result = []
    for a in edges:
        b = edges[a]
        if a not in used:
            result.append((a, b))
            used.add(a); used.add(b)

    print(", ".join(f"({a}, {b})" for a, b in result))
