# overlap alignment
try:
    with open("dataset/rosalind_ba5i.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PAWHEAE
HEAGAWGHEE'''

lines = content.split('\n')
v, w = lines[0], lines[1]

def OverlapAlign1(v, w):
    max_score = -10**9
    max_j = 0
    s = {}
    m, n = len(v), len(w)
    '''
    initialization
    v: matching suffix -> no penalty
    w: matching prefix -> penalize
    '''
    for i in range(m+1):
        s[(i, 0)] = 0
    for j in range(n+1):
        s[(0, j)] = -2 * j
    
    # relaxation
    for i in range(m):
        for j in range(n):
            diagscore = s[(i, j)] + (1 if v[i] == w[j] else -2)
            upscore = s[(i, j+1)] -2
            leftscore = s[(i+1, j)] - 2
            s[(i+1, j+1)] = max(diagscore, upscore, leftscore)
                

    for j in range(n+1):
        if s[(m, j)] > max_score:
            max_score = s[(m, j)]
            max_j = j
            
    # backtracking
    i, j = m, max_j
    align_v, align_w = "", ""
    while i>0 and j>0:
        diagscore = s[(i-1, j-1)] + (1 if v[i-1] == w[j-1] else -2)
        upscore = s[(i-1, j)] -2
        leftscore = s[(i, j-1)] - 2
        curr = s[(i, j)]
                
        if curr == diagscore:
        # if diagscore >= upscore and diagscore >= leftscore:
            align_v = v[i-1] + align_v
            align_w = w[j-1] + align_w
            i -= 1
            j -= 1
        elif curr == upscore:
        # elif upscore >= diagscore and upscore >= leftscore:
            align_v = v[i-1] + align_v
            align_w = "-" + align_w
            i -= 1
        elif curr == leftscore:
        # elif leftscore >= diagscore and leftscore >= upscore:
            align_v = "-" + align_v
            align_w = w[j-1] + align_w
            j -= 1
        else: 
            print("Oops")
            break
            
    return max_score, align_v, align_w

def OverlapAlign2(v, w):
    m, n = len(v), len(w)
    s = [[0]*(n+1) for _ in range(m+1)] 
    d = [[0]*(n+1) for _ in range(m+1)] 
    
    # 1. Initialization
    # w의 prefix 정렬을 위해 첫 행 페널티 부여 + 방향은 왼쪽('l')으로 설정
    for j in range(1, n+1):
        s[0][j] = -2 * j
        d[0][j] = "l" # 맨 윗줄에 도달하면 왼쪽으로 가도록 길을 터줌
    
    # v의 suffix 정렬이므로 첫 열(i행 0열)은 0점, 방향은 위('u')로 설정 (사실 j=0이면 끝나므로 중요하진 않음)
    for i in range(1, m+1):
        d[i][0] = "u"

    # 2. Relaxation
    # 1부터 m, 1부터 n까지 돌면서 인덱스 통일
    for i in range(1, m+1):
        for j in range(1, n+1):
            # 문자열은 0-index이므로 i-1, j-1 사용
            match = 1 if v[i-1] == w[j-1] else -2
            
            diagscore = s[i-1][j-1] + match
            upscore = s[i-1][j] - 2
            leftscore = s[i][j-1] - 2
            
            s[i][j] = max(diagscore, upscore, leftscore)
            
            # 방향 기록
            if s[i][j] == diagscore:
                d[i][j] = "d"
            elif s[i][j] == upscore:
                d[i][j] = "u"
            else:
                d[i][j] = "l"
                
    # 3. Find Max Score
    max_score = -float('inf')
    max_j = 0     
    for j in range(n+1):
        if s[m][j] >= max_score: # >= 를 써서 가능한 긴 정렬 선호
            max_score = s[m][j]
            max_j = j
        
    # 4. Backtrack
    # s 테이블 인덱스 그대로 시작
    i, j = m, max_j
    align_v, align_w = "", ""
    
    # Overlap Alignment는 w의 시작점(j=0)에 도달하면 끝남
    while j > 0:
        if d[i][j] == "d":
            align_v = v[i-1] + align_v
            align_w = w[j-1] + align_w
            i -= 1
            j -= 1
        elif d[i][j] == "u":
            align_v = v[i-1] + align_v
            align_w = "-" + align_w
            i -= 1
        elif d[i][j] == "l":
            align_v = "-" + align_v
            align_w = w[j-1] + align_w
            j -= 1
        else:
            # 이론상 여기에 도달하면 안 됨 (초기화를 잘 했으므로)
            break
            
    return max_score, align_v, align_w
            
max_score, align_v, align_w = OverlapAlign2(v, w)
print(max_score, align_v, align_w, sep="\n")