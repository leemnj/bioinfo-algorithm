# Affine Gap Penalties
try:
    with open("dataset/rosalind_ba5j.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PRTEINS
PRTWPSEIN'''

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

def AffineGap(v, w):
    m, n = len(v), len(w)
    # initiation
    '''
    lower: v에서 gap opening
    middle: match/mismatch
    upper: w에서 gap opening
    '''
    gap_open, gap_extend = -11, -1
    inf = -float('inf')
    lower = [[inf]*(n+1) for _ in range(m+1)]
    upper = [[inf]*(n+1) for _ in range(m+1)]
    middle = [[inf]*(n+1) for _ in range(m+1)]

    middle[0][0] = 0
    for i in range(m):
        lower[i+1][0] = gap_open + i * gap_extend
        middle[i+1][0] = lower[i+1][0]

    for j in range(n):
        upper[0][j+1] = gap_open + j * gap_extend
        middle[0][j+1] = upper[0][j+1]

    # relaxation
    for i in range(m):
        for j in range(n):
            extend_lower = lower[i][j+1] + gap_extend
            start_lower = middle[i][j+1] + gap_open
            lower[i+1][j+1] = max(extend_lower, start_lower)

            extend_upper = upper[i+1][j] + gap_extend
            start_upper = middle[i+1][j] + gap_open
            upper[i+1][j+1] = max(extend_upper, start_upper)

            score = score_matrix[(v[i], w[j])]

            match_from_middle = middle[i][j] + score
            match_from_lower = lower[i][j] + score
            match_from_upper = upper[i][j] + score
            
            middle[i+1][j+1] = max(match_from_lower, match_from_middle, match_from_upper)

    max_score = max(middle[m][n], lower[m][n], upper[m][n])

    # backtracking
    '''
    구조적으로 middle을 거쳐야 함
    e.g.
    A-
    -T
    이렇게 연달아 gap open이 일어나는 것 보다
    A
    T
    mismatch로 가는게 score가 더 클 수 밖에 없어서
    '''
    align_v, align_w = "", ""
    i, j = m, n

    if max_score == lower[m][n]:
        state = "lower"
    elif max_score == upper[m][n]:
        state = "upper"
    else: state = "middle"

    while i>0 or j>0:
        if state == "lower":
            align_v = v[i-1] + align_v
            align_w = "-" + align_w
            if i > 1 and lower[i][j] == lower[i-1][j] + gap_extend:
                state = "lower"
            else:
                state = "middle"
            i -= 1
            
        elif state == "upper":
            align_v = "-" + align_v
            align_w = w[j-1] + align_w
            if j > 1 and upper[i][j] == upper[i][j-1] + gap_extend:
                state = "upper"
            else:
                state = "middle"
            j -= 1
            
        else: # state == "middle"
            align_v = v[i-1] + align_v
            align_w = w[j-1] + align_w
            score = score_matrix.get((v[i-1], w[j-1]), -1)
            
            if middle[i][j] == lower[i-1][j-1] + score:
                state = "lower"
            elif middle[i][j] == upper[i-1][j-1] + score:
                state = "upper"
            else:
                state = "middle"
            i -= 1
            j -= 1

    return max_score, align_v, align_w
print(*AffineGap(v, w), sep="\n")