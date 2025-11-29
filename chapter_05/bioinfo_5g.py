# Edit Distance
try:
    with open("Chapter_5/rosalind_ba5g.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PLEASANTLY
MEANLY
'''

lines = content.split('\n')
v, w = lines[0], lines[1]
n, m = len(v), len(w)

# max length - LCS length (fail)
def LCSlength(v, w):
    n, m = len(v), len(w)
    s = {}
    for i in range(n+1):
        s[(i, 0)] = 0
    for j in range(m+1):
        s[(0, j)] = 0

    for i in range(n):
        for j in range(m):
            if v[i] == w[j]:
                s[(i+1, j+1)] = s[(i, j)] + 1
            else:
                s[(i+1, j+1)] = max(s[(i+1, j)], s[(i, j+1)])
    return int(s[(n, m)])

LCS_LENGTH = LCSlength(v, w)
EDIT_LENGTH = max(m, n) - LCS_LENGTH
# print(EDIT_LENGTH)

# DP
def EditLength(v, w):
    n, m = len(v), len(w)
    dp = {}
    for i in range(n+1):
        dp[(i, 0)] = i
    for j in range(m+1):
        dp[(0, j)] = j

    for i in range(n):
        for j in range(m):
            if v[i]==w[j]:
                dp[(i+1, j+1)] = dp[(i, j)]
            else:
                # insertion, deletion, substitution(diag)
                dp[(i+1, j+1)] = min(dp[(i, j+1)], dp[(i+1, j)], dp[(i, j)]) + 1
    return dp[(n, m)]
print(EditLength(v, w))