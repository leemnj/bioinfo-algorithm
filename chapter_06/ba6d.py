# BA6D: Implement 2-Break Sorting
def parse_genome(genome_str):
    """
    (+1 -2 -3) 형태의 문자열을 정수 리스트의 리스트로 파싱합니다.
    Example: "(+1 -2 -3)(+4 +5)" -> [[1, -2, -3], [4, 5]]
    """
    chromosomes = []
    parts = genome_str.strip().split('(')
    for part in parts:
        if not part: continue
        # ')' 제거 및 숫자 파싱
        nums = list(map(int, part.replace(')', '').split()))
        chromosomes.append(nums)
    return chromosomes

def chromosome_to_cycle(chromosome):
    """
    염색체(블록 리스트)를 노드 시퀀스로 변환합니다.
    Block k -> Nodes 2k-1, 2k
    +k: 2k-1 -> 2k (정방향)
    -k: 2k -> 2k-1 (역방향)
    반환되는 노드 리스트는 Head -> Tail 순서입니다.
    """
    nodes = []
    for block in chromosome:
        if block > 0:
            nodes.append(2 * block - 1)
            nodes.append(2 * block)
        else:
            nodes.append(2 * abs(block))
            nodes.append(2 * abs(block) - 1)
    return nodes

def genome_to_edges(chromosomes):
    """
    유전체(염색체 리스트)를 Colored Edges(인접한 블록 간의 연결) 집합으로 변환합니다.
    반환 형식: Dictionary {node: neighbor}
    """
    edges = {}
    for chrom in chromosomes:
        nodes = chromosome_to_cycle(chrom)
        n = len(nodes)
        # 염색체 내의 인접한 블록들을 연결 (블록의 Tail -> 다음 블록의 Head)
        # nodes 배열은 [Head1, Tail1, Head2, Tail2, ...] 형태임
        # 따라서 Tail1(idx 1) -> Head2(idx 2), Tail2(idx 3) -> Head3(idx 4)...
        for j in range(1, n, 2):
            u = nodes[j]
            v = nodes[(j + 1) % n] # 원형 연결
            edges[u] = v
            edges[v] = u
    return edges

def edges_to_genome(edges):
    """
    Colored Edges 집합을 다시 유전체 문자열로 복원합니다.
    """
    visited = set()
    chromosomes = []
    
    # 노드 1부터 순차적으로 방문하며 사이클 찾기
    # edges의 key들은 노드 번호들임
    for node in sorted(edges.keys()):
        if node in visited:
            continue
            
        cycle = []
        # 사이클 순회 시작
        # 임의의 노드(보통 Head인 2k-1에서 시작하는 것이 편함)에서 시작해야 하지만,
        # 여기서는 edges에 있는 연결(Synteny 간 연결)을 따라가야 함.
        
        # 시작 노드 설정 (현재 node가 Tail인지 Head인지 중요하지 않음, 순환하므로)
        curr = node
        
        while curr not in visited:
            visited.add(curr)
            
            # 1. 현재 노드가 속한 블록 식별 및 방향 결정
            if curr % 2 == 0:
                block_id = curr // 2
                # 짝수 노드(2k)는 +k의 Tail 또는 -k의 Head
                # 경로 복원을 위해: Tail에서 들어왔다고 가정하면 역방향(-k)으로 나감
                # 하지만 여기서는 "edges"가 Synteny Block 사이의 연결이므로
                # Synteny Block "내부"를 가로질러 반대편 노드로 이동해야 함.
                
                # 들어온 곳이 2k(짝수) -> 블록 내부는 (2k, 2k-1)로 연결됨 -> -k 방향
                cycle.append(-block_id)
                next_node_in_block = curr - 1
            else:
                block_id = (curr + 1) // 2
                # 홀수 노드(2k-1) -> 블록 내부는 (2k-1, 2k)로 연결됨 -> +k 방향
                cycle.append(block_id)
                next_node_in_block = curr + 1
            
            visited.add(next_node_in_block)
            
            # 2. Synteny Block을 건너뛰어 다음 연결된 엣지 찾기
            if next_node_in_block in edges:
                curr = edges[next_node_in_block]
            else:
                break # Should not happen in complete cycle
        
        chromosomes.append(cycle)
        
    # 문자열 포맷팅
    result_str = []
    for chrom in chromosomes:
        parts = []
        for block in chrom:
            if block > 0: parts.append(f"+{block}")
            else: parts.append(f"{block}")
        result_str.append(f"({' '.join(parts)})")
        
    return "".join(result_str)

def two_break_on_genome_graph(edges, u, v, x, y):
    """
    그래프 상에서 2-Break 수행
    기존 엣지 (u, x), (v, y) 삭제 -> (u, v), (x, y) 추가
    (주의: 입력 u, v는 연결하고 싶은 목표 엣지)
    """
    # 기존 연결 삭제
    # u와 x가 연결되어 있고, v와 y가 연결되어 있음
    del edges[u]; del edges[x]
    del edges[v]; del edges[y]
    
    # 새로운 연결 추가 (u-v, x-y)
    edges[u] = v; edges[v] = u
    edges[x] = y; edges[y] = x

def solve_2_break_sorting(P_str, Q_str):
    # 1. 그래프 생성
    chroms_P = parse_genome(P_str)
    chroms_Q = parse_genome(Q_str)
    
    edges_P = genome_to_edges(chroms_P) # Red edges
    edges_Q = genome_to_edges(chroms_Q) # Blue edges
    
    # 초기 상태 출력
    print(P_str)
    
    # 2. Greedy Loop
    # Q의 엣지(Blue)를 하나씩 P에 강제로 적용
    for u in edges_Q:
        # 무방향 그래프이므로 중복 방지 (u < v일 때만 처리하거나, 처리된 엣지 건너뛰기)
        v = edges_Q[u]
        if u > v: continue 
        
        # 만약 P에 이미 (u, v)가 있다면 패스 (Trivial cycle)
        if edges_P.get(u) == v:
            continue
            
        # P에는 (u, x)와 (v, y)가 있을 것임
        x = edges_P[u]
        y = edges_P[v]
        
        # 2-Break 수행: (u, x), (v, y) -> (u, v), (x, y)
        two_break_on_genome_graph(edges_P, u, v, x, y)
        
        # 중간 결과 출력
        print(edges_to_genome(edges_P))
        
# --- 실행부 ---
if __name__ == "__main__":
    # Rosalind Sample Dataset
    
    
    # 파일 입력 예시
    try:
        with open("input/rosalind_ba6d.txt") as f:
            lines = f.readlines()
            P = lines[0].strip()
            Q = lines[1].strip()
    except :
        P = "(+1 -2 -3 +4)"
        Q = "(+1 +2 -4 -3)" 

    solve_2_break_sorting(P, Q)