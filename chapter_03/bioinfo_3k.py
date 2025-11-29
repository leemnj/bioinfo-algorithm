# BA3K: Generate Contigs from a Collection of Reads
'''
contig: maximal non-branching path
sequencing 결과에서 겹쳐져서 확실하게 이어지는 연속적인 구간
indegree = outdegree = 1인 node들로 이루어진 path
'''

from collections import defaultdict
from textwrap import dedent

def build_DBG(reads):
    """
    De Bruijn Graph 생성 및 차수 계산 (초기 상태 고정)
    """
    graph = defaultdict(list)
    indegree = defaultdict(int)
    outdegree = defaultdict(int)
    
    for kmer in reads:
        u = kmer[:-1]
        v = kmer[1:]
        
        graph[u].append(v)
        outdegree[u] += 1
        indegree[v] += 1
        
        # 딕셔너리 키 초기화 (모든 노드가 키로 존재하도록)
        if v not in outdegree: outdegree[v] = 0
        if u not in indegree: indegree[u] = 0

    return graph, indegree, outdegree

def get_contigs_from_DBG(graph, indegree, outdegree):
    """
    고정된 차수(Degree) 정보를 기반으로 Contig 추출
    (그래프의 엣지를 소모하지만, 차수 정보는 변하지 않음)
    """
    contigs = []
    
    # 그래프의 모든 노드 리스트
    nodes = list(graph.keys())
    
    # ---------------------------------------------------------
    # [Step 1] "분기점"에서 시작하는 Contig 찾기
    # 분기점 정의: in != 1 또는 out != 1 인 노드
    # 이 노드들은 절대 Contig의 '중간'이 될 수 없으므로, 여기서 시작해야 안전함.
    # ---------------------------------------------------------
    for v in nodes:
        # 1-in-1-out(단순 통로)가 '아닌' 노드만 골라서 시작점으로 삼음
        if not (indegree[v] == 1 and outdegree[v] == 1):
            if outdegree[v] > 0:
                # 해당 노드에서 나가는 모든 엣지를 각각의 Contig 시작으로 봄
                # while 루프를 사용하여 graph[v] 리스트를 비워나감 (방문 처리)
                while graph[v]:
                    w = graph[v].pop(0) # 엣지 (v -> w) 소모
                    path = [v, w]
                    
                    # 현재 경로의 끝점(w)에서 계속 직진 가능한지 확인
                    # 주의: 여기서 w의 차수는 '초기 계산된 값'을 그대로 참조함
                    curr = w
                    while indegree[curr] == 1 and outdegree[curr] == 1:
                        # 1-in-1-out이라도 엣지가 남아있어야 이동 가능
                        if not graph[curr]: 
                            break
                            
                        next_node = graph[curr].pop(0) # 엣지 소모
                        path.append(next_node)
                        curr = next_node
                    
                    contigs.append(path)

    # ---------------------------------------------------------
    # [Step 2] 고립된 사이클(Isolated Cycles) 찾기
    # Step 1을 거치고도 그래프에 엣지가 남아있다면, 
    # 그것은 모든 노드가 1-in-1-out인 순환 고리들임.
    # ---------------------------------------------------------
    for v in nodes:
        while graph[v]: # 아직 방문 안 한 엣지가 있다면
            w = graph[v].pop(0)
            path = [v, w]
            
            curr = w
            while indegree[curr] == 1 and outdegree[curr] == 1:
                if not graph[curr]:
                    break
                next_node = graph[curr].pop(0)
                path.append(next_node)
                curr = next_node
            
            contigs.append(path)

    # ---------------------------------------------------------
    # [Step 3] 경로(Node List)를 문자열로 변환
    # ---------------------------------------------------------
    result_strings = []
    for path in contigs:
        contig_str = path[0]
        for node in path[1:]:
            contig_str += node[-1] # 뒷 노드의 마지막 글자만 추가
        result_strings.append(contig_str)
        
    return sorted(result_strings)
    
if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3k.txt") as f:
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
    contigs = sorted(get_contigs_from_DBG(DBG, indegree, outdegree))
    print(' '.join(contigs))
    with open("output/3K.txt", "w") as f:
        f.write(' '.join(contigs))