with open('Bioinfo algorithm/Chapter_1/rosalind_ba1g.txt', "r") as f:
    content = f.read()

# content = '''GGGCCGTTGGT
# GGACCGTTGAC'''
seq1, seq2, _ = content.split('\n')

cnt = 0
for i in range(len(seq1)):
    if seq1[i] != seq2[i]:
        cnt += 1

print(cnt)