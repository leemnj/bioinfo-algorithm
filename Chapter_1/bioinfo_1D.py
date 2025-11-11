pattern, seq = 'GTCGAATGT', 'GATATATGCATATACTT'

def FindAllOccur(seq, pattern):
    idx = []
    for i in range(len(seq) - len(pattern) + 1):
        if seq[i:i+len(pattern)] == pattern:
            idx.append(i)
    return idx

# print(FindAllOccur(seq, pattern))
for i in FindAllOccur(seq, pattern):
    print(i, end = ' ')