# fitting algorithm
try:
    with open("Chapter_5/rosalind_ba5h.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''GTAGGCTTAAGGTTA
TAGATA'''

lines = content.split('\n')
v, w = lines[0], lines[1]

def FittingAlignment(v, w):
    '''
    initiation
    w를 다 써야되니까 j 쪽은 -1씩
    시작은 어느 부분에서 하든 penalty 없어야 하니까 i 쪽은 0
    '''
    n, m = len(v), len(w)
    s = {}
    for i in range(n+1):
        s[(i, 0)] = 0
    for j in range(m+1):
        s[(0, j)] = -j
    max_score = 0
    max_i = 0

    '''
    relaxation
    indel, substitution 고려해서 왼쪽 위 대각선방향에서 -1한 값 중 최대

    '''
    for i in range(n):
        for j in range(m):
            if v[i] == w[j]:
                s[(i+1, j+1)] = s[(i, j)] + 1
            else:
                s[(i+1, j+1)] = max(s[(i, j+1)], s[(i+1, j)], s[(i, j)]) - 1
        if s[(i+1, m)] > max_score:
            max_score = s[(i+1, m)]
            max_i = i+1

    i, j = max_i, m
    align_v = ""
    align_w = ""
    while(i > 0 and j > 0):
        upscore = s[(i-1, j)]
        leftscore = s[(i, j-1)]
        diagscore = s[(i-1, j-1)]
        if v[i-1] == w[j-1] or (diagscore >= upscore and diagscore >= leftscore):
            align_v = v[i-1] + align_v
            align_w = w[j-1] + align_w
            i -= 1
            j -= 1
        elif upscore >= leftscore and upscore >= diagscore:
            align_v = v[i-1] + align_v
            align_w = "-" + align_w
            i -= 1
        elif leftscore >= upscore and leftscore >= diagscore:
            align_v = "-" + align_v
            align_w = w[j-1] + align_w
            j -=1

    return max_score, align_v, align_w

print(*FittingAlignment(v, w), sep="\n")