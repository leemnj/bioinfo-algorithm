# Local alignment
try:
    with open("Chapter_5/rosalind_ba5f.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''MEANLY
PENALTY
'''

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
score_matrix = load_score_matrix("PAM250.txt")

lines = content.split('\n')
AA1, AA2 = lines[0], lines[1]

n, m = len(AA1), len(AA2)
dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
path = [[None for _ in range(m+1)] for _ in range(n+1)]

sigma = 5
max_score = 0
max_i, max_j = 0, 0

for i in range(1, n+1):
    for j in range(1, m+1):
        v = AA1[i-1]
        w = AA2[j-1]

        diag_score = dp[i-1][j-1] + score_matrix[(v, w)]
        up_score = dp[i-1][j] - sigma
        left_score = dp[i][j-1] - sigma

        if diag_score >= up_score and diag_score >= left_score and diag_score >= 0:
            dp[i][j] = diag_score
            path[i][j] = "d" 
        elif up_score >= left_score and up_score >= 0:
            dp[i][j] = up_score
            path[i][j] = "u"
        elif left_score >= 0:
            dp[i][j] = left_score
            path[i][j] = "l"
        else:
            dp[i][j] = 0
            path[i][j] = "stop"

        if dp[i][j] > max_score:
            max_score = dp[i][j]
            max_i = i
            max_j = j

# Backtracking
align_v = ""
align_w = ""

## i, j = n, m
i, j = max_i, max_j
while i>0 or j>0:
    direction = path[i][j]
    if direction == "stop" or direction is None:
        break
    if direction == "d":
        align_v += AA1[i-1]
        align_w += AA2[j-1]
        i-=1
        j-=1
    elif direction == "u":
        align_v += AA1[i-1]
        align_w += "-"
        i-=1
    elif direction == "l":
        align_v += "-"
        align_w += AA2[j-1]
        j-=1
    else: break
align_v = align_v[::-1] # 순서 반대로
align_w = align_w[::-1]

print(max_score, align_v, align_w, sep='\n')