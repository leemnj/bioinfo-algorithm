# Middle Edge
try:
    with open("dataset/rosalind_ba5k.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PLEASANTLY
MEASNLY'''

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
    """
    선형 공간(Linear Space)을 사용하여 서열 v와 w의 
    Global Alignment 점수 컬럼(마지막 열)만 반환
    """
    n = len(v)
    m = len(w)
    
    curr = [-sigma * i for i in range(n + 1)]
    
    for j in range(1, m + 1):
        prev = curr[:] # 이전 열 저장
        curr[0] = -sigma * j # 첫 행(가로) 초기화
        
        for i in range(1, n + 1):
            # 1. Match/Mismatch (Diagonal)
            score = matrix.get((v[i-1], w[j-1]), -1)
            diag = prev[i-1] + score
            
            # 2. Deletion (Horizontal, w에 gap) -> from up
            horiz = curr[i-1] - sigma
            
            # 3. Insertion (Vertical, v에 gap) -> from left
            vert = prev[i] - sigma
            
            # Global Alignment
            curr[i] = max(diag, horiz, vert)
            
    return curr

def solve_middle_edge(v, w, matrix, sigma=5):
    m = len(w)
    mid = m // 2
    
    # 1. Forward DP: (0,0) 부터 중간 열(mid)까지 계산
    from_source = get_score_column(v, w[:mid], matrix, sigma)
    
    # 2. Backward DP: (n,m) 부터 중간 열 다음(mid+1)까지 역방향 계산
    # w의 오른쪽 절반(w[mid:])을 뒤집어서 사용, v도 뒤집어야 함
    # 결과값인 to_sink도 뒤집혀 나오므로 다시 뒤집어줘야 원래 인덱스(0~n)와 맞음
    reversed_sink = get_score_column(v[::-1], w[mid:][::-1], matrix, sigma)
    to_sink = reversed_sink[::-1]
    
    n = len(v)
    max_score = -float('inf')
    middle_edge = None
    
    # 3. Middle Edge 찾기
    # w[mid] 문자를 지나가는 대각선 혹은 수평 엣지를 검사
    
    for i in range(n): # diagonal
        score = from_source[i] + matrix.get((v[i], w[mid]), -1) + to_sink[i+1]
        
        if score > max_score:
            max_score = score
            middle_edge = ((i, mid), (i+1, mid+1))
            
    for i in range(n + 1): # up
        score = from_source[i] - sigma + to_sink[i]
        
        if score > max_score:
            max_score = score
            middle_edge = ((i, mid), (i, mid+1))
            
    return middle_edge

print(*solve_middle_edge(v, w, score_matrix))