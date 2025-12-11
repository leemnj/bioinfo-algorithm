import sys

def parse_genome_to_edges(genome_str):
    """
    문자열 형태의 유전체를 파싱하여 각 노드 간의 연결(Edge) 정보를 딕셔너리로 반환합니다.
    예: (+1 +2 +3) -> {2: 3, 3: 2, 4: 5, 5: 4, 6: 1, 1: 6}
    """
    edges = {}
    chromosomes = genome_str.strip().split('(')
    
    max_block = 0
    
    for chrom in chromosomes:
        if not chrom: continue
        # 괄호 제거 및 블록 분리
        blocks = list(map(int, chrom.replace(')', '').split()))
        
        n = len(blocks)
        for i in range(n):
            curr_block = blocks[i]
            next_block = blocks[(i + 1) % n] # 원형이므로 마지막은 처음과 연결
            
            # 절댓값 최대치 갱신 (전체 블록 개수 n을 구하기 위함)
            max_block = max(max_block, abs(curr_block), abs(next_block))
            
            # 노드 번호 매핑 (블록 k -> 2k-1, 2k)
            # +k: Tail은 2k
            # -k: Tail은 2k-1
            if curr_block > 0:
                curr_tail = 2 * curr_block
            else:
                curr_tail = 2 * abs(curr_block) - 1
            
            # +k: Head는 2k-1
            # -k: Head는 2k
            if next_block > 0:
                next_head = 2 * next_block - 1
            else:
                next_head = 2 * abs(next_block)
            
            # 양방향 연결 (무방향 그래프)
            edges[curr_tail] = next_head
            edges[next_head] = curr_tail
            
    return edges, max_block

def solve_2_break_distance(p_str, q_str):
    # 1. 각 유전체의 엣지 정보 생성
    edges_p, n = parse_genome_to_edges(p_str)
    edges_q, _ = parse_genome_to_edges(q_str)
    
    # 2. 사이클 개수 세기 (Breakpoint Graph)
    # 노드는 1부터 2n까지 존재
    visited = set()
    cycles = 0
    
    for i in range(1, 2 * n + 1):
        if i not in visited:
            cycles += 1
            curr = i
            while curr not in visited:
                visited.add(curr)
                
                # P 그래프의 엣지를 따라감 (빨간 선)
                # P에서 curr와 연결된 노드 찾기
                next_node_p = edges_p[curr]
                visited.add(next_node_p)
                
                # Q 그래프의 엣지를 따라감 (파란 선)
                # P에서 도착한 곳(next_node_p)에서 Q의 엣지를 타고 이동
                next_node_q = edges_q[next_node_p]
                
                # 다음 루프를 위해 현재 위치 갱신
                curr = next_node_q
                
    # 3. 2-Break Distance 정리: blocks - cycles
    return n - cycles

# --- 실행부 ---
if __name__ == "__main__":
    # 데이터 입력
    # rosalind_ba6c.txt 파일이 있다면 읽어서 처리
    try:
        with open("input/rosalind_ba6c.txt", "r") as f:
            lines = f.readlines()
            P = lines[0].strip()
            Q = lines[1].strip()
            
        result = solve_2_break_distance(P, Q)
        print(result)
        
    except FileNotFoundError:
        # 테스트용 데이터 (Sample Dataset)
        sample_P = "(+1 +2 +3 +4 +5 +6)"
        sample_Q = "(+1 -3 -6 -5)(+2 -4)"
        print(f"Sample Result: {solve_2_break_distance(sample_P, sample_Q)}")