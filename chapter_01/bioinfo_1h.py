try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1h.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''ATTCTGGA
CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAATGCCTAGCGGCTTGTGGTTTCTCCTACGCTCC
3
'''

content = content.split('\n')
pattern = content[0]
seq = content[1]
mismatch = int(content[2])

def HammingDist(seq1, seq2):
    cnt = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            cnt += 1
    return cnt

def PatternMatch(pattern, seq, mismatch):
    length = len(pattern)
    pos_list = []
    for i in range(len(seq)-length+1):
        if(HammingDist(pattern, seq[i:i+length]) <= mismatch):
            # pos_list.append(i)
            pos_list.append(str(i))
    # return pos_list
    return ' '.join(pos_list)

# for pos in PatternMatch(pattern, seq, mismatch) :
#     print(pos, end = ' ')
print(PatternMatch(pattern, seq, mismatch))