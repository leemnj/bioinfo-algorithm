# Global alignment
try:
    with open("Chapter_5/rosalind_ba5e.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PLEASANTLY
MEANLY'''

lines = content.split('\n')
AA1, AA2 = lines[0], lines[1]

# parsing BLOSUM62
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
# print(score_matrix[('A', 'K')])

# dp initiation
n, m = len(AA1), len(AA2)
dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
path = [[None for _ in range(m+1)] for _ in range(n+1)]

sigma = 5

for i in range(1, n+1):
    dp[i][0] = dp[i-1][0] - sigma
    path[i][0] = "u" # up

for j in range(1, m+1):
    dp[0][j] = dp[0][j-1] - sigma
    path[0][j] = "l" # left

# relaxation
for i in range(1, n+1):
    for j in range(1, m+1):
        v = AA1[i-1]
        w = AA2[j-1]

        diag_score = dp[i-1][j-1] + score_matrix[(v, w)]
        up_score = dp[i-1][j] - sigma
        left_score = dp[i][j-1] - sigma

        if diag_score >= up_score and diag_score >= left_score:
            dp[i][j] = diag_score
            path[i][j] = "d" # diag
        elif up_score >= left_score:
            dp[i][j] = up_score
            path[i][j] = "u"
        else:
            dp[i][j] = left_score
            path[i][j] = "l"
max_score = dp[n][m]

# backtracking
align_v = ""
align_w = ""

i, j = n, m

while i>0 or j>0:
    direction = path[i][j]
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
align_v = align_v[::-1] # 순서 반대로
align_w = align_w[::-1]

print(max_score, align_v, align_w, sep='\n')
