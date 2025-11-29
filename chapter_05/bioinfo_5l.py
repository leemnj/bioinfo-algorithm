# Global Alignment in Linear Space
try:
    with open("inputs/rosalind_ba5l.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PLEASANTLY
MEANLY'''

lines = content.split("\n")
v, w = lines[0], lines[1]

def load_score_matrix(path):
    scores = {}
    with open(path, 'r') as f:
        header = f.readline()
        columns = header.strip().split()
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split()
            row, values = parts[0], parts[1:]
            for i in range(len(columns)):
                col = columns[i]
                score = int(values[i])

                scores[(row, col)] = score
                scores[(col, row)] = score
    return scores
score_matrix = load_score_matrix("BLOSUM62.txt")

def get_score_column(v, w, matrix, sigma=5):
    """한 쪽 방향으로 점수만 계산하여 마지막 열을 반환 (Linear Space)"""
    n = len(v)
    m = len(w)
    
    # 첫 열 초기화 (v에 대한 Gap penalty)
    curr = [-sigma * i for i in range(n + 1)]
    
    for j in range(1, m + 1):
        prev = curr[:]
        curr[0] = -sigma * j
        
        for i in range(1, n + 1):
            score = matrix.get((v[i-1], w[j-1]), -1)
            diag = prev[i-1] + score
            horiz = curr[i-1] - sigma # v gap (deletion)
            vert = prev[i] - sigma    # w gap (insertion)
            curr[i] = max(diag, horiz, vert)
            
    return curr

def LinearSpaceAlignment(v, w, matrix, sigma=5):
    """Hirschberg's Algorithm을 이용한 재귀적 정렬"""
    
    # --- Base Cases ---
    if len(v) == 0:
        return -sigma * len(w), "-" * len(w), w
    if len(w) == 0:
        return -sigma * len(v), v, "-" * len(v)
        
    # --- Recursive Step ---
    # 1. w를 반으로
    mid = len(w) // 2
    
    # 2. Forward & Backward Score
    # from_source: v 전체 vs w의 왼쪽 절반 (mid까지)
    from_source = get_score_column(v, w[:mid], matrix, sigma)
    
    # to_sink: v 전체(뒤집힘) vs w의 오른쪽 절반(뒤집힘)
    to_sink = get_score_column(v[::-1], w[mid+1:][::-1], matrix, sigma)[::-1]
    
    # 3. Middle Edge
    # mid 열(from_source)에서 mid+1 열(to_sink)로 가는 최적의 경로 찾기
    n = len(v)
    max_score = -float('inf')
    split_idx = -1
    edge_type = "" # "DIAG" or "HORIZ" (w 입장에서의 Horizontal = v Gap)
    
    # w[mid] 문자를 어떻게 처리할 것인가?
    # w[mid]는 w의 (mid)번째 인덱스 문자. 이 문자가 v의 문자와 매칭되거나(DIAG), v의 Gap이 됨(HORIZ).
    
    w_char = w[mid]
    
    # 모든 가능한 v의 위치 i에 대해 검사
    for i in range(n + 1):
        # Case A: Diagonal Edge (v[i]와 w[mid] 매칭) -> v 인덱스 1 증가
        if i < n:
            score_diag = from_source[i] + matrix.get((v[i], w_char), -1) + to_sink[i+1]
            if score_diag > max_score:
                max_score = score_diag
                split_idx = i
                edge_type = "DIAG"
                
        # Case B: Horizontal Edge (w[mid]가 v의 Gap과 매칭) -> v 인덱스 그대로
        # 그래프상 수평 = v는 그대로, w만 진행 = Indel penalty
        score_horiz = from_source[i] - sigma + to_sink[i]
        if score_horiz > max_score:
            max_score = score_horiz
            split_idx = i
            edge_type = "HORIZ"
            
    # 4. 재귀 호출 및 결과 병합
    if edge_type == "DIAG":
        # v[split_idx]와 w[mid]가 매칭됨
        mid_edge_v = v[split_idx]
        mid_edge_w = w[mid]
        
        # 왼쪽 위: v[:split_idx] vs w[:mid]
        score_l, v_l, w_l = LinearSpaceAlignment(v[:split_idx], w[:mid], matrix, sigma)
        # 오른쪽 아래: v[split_idx+1:] vs w[mid+1:]
        score_r, v_r, w_r = LinearSpaceAlignment(v[split_idx+1:], w[mid+1:], matrix, sigma)
        
    else: # HORIZ
        # v에는 Gap, w[mid] 사용
        mid_edge_v = "-"
        mid_edge_w = w[mid]
        
        # 왼쪽 위: v[:split_idx] vs w[:mid]
        score_l, v_l, w_l = LinearSpaceAlignment(v[:split_idx], w[:mid], matrix, sigma)
        # 오른쪽 아래: v[split_idx:] vs w[mid+1:] (v 인덱스 증가 안 함)
        score_r, v_r, w_r = LinearSpaceAlignment(v[split_idx:], w[mid+1:], matrix, sigma)

    return max_score, v_l + mid_edge_v + v_r, w_l + mid_edge_w + w_r

score, aligned_v, aligned_w = LinearSpaceAlignment(v, w, score_matrix, sigma=5)
            
print(score)
print(aligned_v)
print(aligned_w)