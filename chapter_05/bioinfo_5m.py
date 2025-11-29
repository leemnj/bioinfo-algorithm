# Multiple Sequence Alignment
try:
    with open("inputs/rosalind_ba5m.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''ATATCCG
TCCGA
ATGTACTG'''

lines = content.split("\n")
v, w, u = lines[0], lines[1], lines[2]

def MSA(v, w, u):
    n, m, l = len(v), len(w), len(u)
    s = [[[0 for _ in range(l+1)] for _ in range(m+1)] for _ in range(n+1)]

    for i in range(n):
        for j in range(m):
            for k in range(l):
                if v[i] == w[j] == u[k]:
                    s[i+1][j+1][k+1] = s[i][j][k] + 1
                else:
                    s[i+1][j+1][k+1] = max(s[i+1][j][k],
                                           s[i][j+1][k],
                                           s[i][j][k+1],
                                           s[i+1][j+1][k],
                                           s[i+1][j][k+1],
                                           s[i][j+1][k+1])
    score = s[n][m][l]

    align_v, align_w, align_u = "", "", ""
    i, j, k = n, m, l

    while i>0 or j>0 or k>0:
        if i > 0 and j > 0 and k > 0 and s[i][j][k] == s[i-1][j-1][k-1] + 1 and v[i-1] == w[j-1] == u[k-1]:
            align_v = v[i-1] + align_v
            align_w = w[j-1] + align_w
            align_u = u[k-1] + align_u
            i -= 1; j -= 1; k -= 1
        elif i > 0 and s[i][j][k] == s[i-1][j][k]:
            align_v = v[i-1] + align_v
            align_w = "-" + align_w
            align_u = "-" + align_u
            i -= 1
        elif j > 0 and s[i][j][k] == s[i][j-1][k]:
            align_v = "-" + align_v
            align_w = w[j-1] + align_w
            align_u = "-" + align_u
            j -= 1
        elif k > 0 and s[i][j][k] == s[i][j][k-1]:
            align_v = "-" + align_v
            align_w = "-" + align_w
            align_u = u[k-1] + align_u
            k -= 1
        elif i > 0 and j > 0 and s[i][j][k] == s[i-1][j-1][k]:
             align_v = v[i-1] + align_v
             align_w = w[j-1] + align_w
             align_u = "-" + align_u
             i -= 1; j -= 1
        elif i > 0 and k > 0 and s[i][j][k] == s[i-1][j][k-1]:
             align_v = v[i-1] + align_v
             align_w = "-" + align_w
             align_u = u[k-1] + align_u
             i -= 1; k -= 1
        elif j > 0 and k > 0 and s[i][j][k] == s[i][j-1][k-1]:
             align_v = "-" + align_v
             align_w = w[j-1] + align_w
             align_u = u[k-1] + align_u
             j -= 1; k -= 1

    return score, align_v, align_w, align_u

print(*MSA(v, w, u), sep="\n")