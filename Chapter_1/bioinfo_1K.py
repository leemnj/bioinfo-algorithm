try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1k.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''ACGCGGCTCTGAAA
2
'''
seq, k = content.split()
k = int(k)

def MakeKMer(k):
    k_mer = ['']
    base_list = ['A', 'C', 'G', 'T']
    for _ in range(k):
        new_k_mer = []
        for seq in k_mer:
            for base in base_list:
                new_k_mer.append(seq+base)
        k_mer = new_k_mer
    return k_mer

# print(MakeKMer(3))

'''
그래 이렇게 하고 싶었던 건데
def genDnaKmers(k, s=""):
    if k <= 0:
        return [ s ]
    res = []
    for char in "ACGT":
        res += genDnaKmers(k - 1, s + char) 
    return res
'''

def FreqArray(seq, k):
    k_mer = MakeKMer(k)
    freq = []
    for pattern in k_mer:
        cnt = 0
        for i in range(len(seq)-k+1):
            if seq[i:i+k] == pattern:
                cnt += 1
    #     freq.append(str(cnt))
    # return ' '.join(freq)
        freq.append(cnt)
    return ' '.join(str(x) for x in freq)

print(FreqArray(seq, k))