# import os
# file = os.open('Bioinfo algorithm/rosalind_ba1f.txt')

# seq = 'CCTATCGGTGGATTAGCATGTCCCTGTACGTTTCGCCGCGAACTAGTTCACACGGCTTGATGGCAAATGGTTTTTCCGGCGACCGTAATCGTCCACCGAG'

with open('Bioinfo algorithm/rosalind_ba1f.txt', "r") as f:
    content = f.read()

'''
# 1. too much high complexity
'''
# def count(subseq, char):
#         cnt = 0
#         for c in subseq:
#             if c == char : cnt += 1
#         return cnt

# def FindPos(seq):

#     skews = []
#     for i in range(len(seq)):
#         subseq = seq[:i]
#         skew = count(subseq, 'G') - count(subseq, 'C')
#         skews.append(skew)
    
#     min = 0
#     for i in range(len(skews)):
#         if min > skews[i] : min = skews[i]
#     pos = [i for i, value in enumerate(skews) if value == min]
#     return pos

# print(FindPos(content))

'''
# 2. Optimal
'''
content = content.replace('\n', '')

def minimumSkews (sequence):
    skews = [0]
    values = {'A':0,'T':0,'C':-1,'G':1}
    for base in sequence:
        skews.append(skews[-1] + values[base])
    minimum = min(skews)
    indices = [str(i) for i, v in enumerate(skews) if v == minimum]
    return ' '.join(indices)

print(minimumSkews(content))