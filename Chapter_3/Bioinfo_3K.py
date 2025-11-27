# BA3K: Generate Contigs from a Collection of Reads
'''
contig: maximal non-branching path
sequencing 결과에서 겹쳐져서 확실하게 이어지는 연속적인 구간
indegree = outdegree = 1인 node들로 이루어진 path
'''

from collections import defaultdict
from textwrap import dedent

def build_DBG(reads):
    graph, indegree, outdegree = defaultdict(list), defaultdict(int), defaultdict(int)
    for read in reads:
        prefix = read[:-1]
        suffix = read[1:]
        graph[prefix].append(suffix)
        
        outdegree[prefix] += 1
        indegree[suffix] += 1
        
        if suffix not in graph:
            graph[suffix] = []

    return graph, indegree, outdegree

def get_contigs_from_DBG(graph, indegree, outdegree):
    contigs = []
    
    # 원본 보존 + defaultdict 유지
    g = {u: list(vs) for u, vs in graph.items()}
    in_deg = defaultdict(int, indegree)
    out_deg = defaultdict(int, outdegree)

    nodes = set(g.keys()) | set(in_deg.keys()) | set(out_deg.keys())

    def consume_edge(u, v):
        """ edge 사용 → 제거 + indegree/outdegree 감소 """
        g[u].remove(v)
        out_deg[u] -= 1
        in_deg[v] -= 1
        return v

    # ---- 1) branching start node들 먼저 확장 ----
    for node in nodes:
        if out_deg[node] > 0 and not (in_deg[node] == 1 and out_deg[node] == 1):
            while out_deg[node] > 0:
                path = [node]
                cur = node

                # 시작 edge 하나 소모
                nxt = g[cur][0]
                cur = consume_edge(cur, nxt)
                path.append(cur)

                # indegree=outdegree=1 노드면 계속 확장
                while in_deg[cur] == 1 and out_deg[cur] == 1:
                    nxt = g[cur][0]
                    cur = consume_edge(cur, nxt)
                    path.append(cur)

                # k-mer list → 문자열 전환
                seq = path[0] + ''.join(p[-1] for p in path[1:])
                contigs.append(seq)

    # ---- 2) 아직 남아있는 것은 cycle (in=1=out) ----
    for node in nodes:
        while out_deg[node] > 0 and in_deg[node] > 0:
            path = [node]
            cur = node

            nxt = g[cur][0]
            cur = consume_edge(cur, nxt)
            path.append(cur)

            while in_deg[cur] == 1 and out_deg[cur] == 1:
                nxt = g[cur][0]
                cur = consume_edge(cur, nxt)
                path.append(cur)

            seq = path[0] + ''.join(p[-1] for p in path[1:])
            contigs.append(seq)

    return contigs
    
if __name__ == "__main__":
    try:
        with open("input/rosalind.ba3k.txt") as f:
            data = f.read().strip().splitlines()
    except:
        data = dedent("""
                    ATG
                    ATG
                    TGT
                    TGG
                    CAT
                    GGA
                    GAT
                    AGA""").strip().splitlines()
    reads = data
    DBG, indegree, outdegree = build_DBG(reads)
    contigs = get_contigs_from_DBG(DBG, indegree, outdegree)
    print(' '.join(contigs))