try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1j.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''ACGTTGCATGTCGCATGATGCATGAGAGCT
4 1
'''

content = content.split()
seq, length, mismatch = content
length, mismatch = int(length), int(mismatch)

def Neighbors(patterns, mismatch):
    '''same as ba1i_subset'''
    neighbor = set()
    for _ in range(mismatch):
        for pattern in patterns:
            for i in range(len(pattern)):        
                for j in ['A', 'T', 'C', 'G']:
                    new_pattern = pattern[:i]+j+pattern[i+1:]
                    neighbor.add(new_pattern)
        patterns = list(neighbor)
    neighbor = list(set(neighbor))
    return neighbor

def HammDist(target, pattern):
    cnt = 0
    for i in range(len(target)):
        if target[i] != pattern[i]:
            cnt += 1
    return cnt

def ReverseComplement(pattern):
    base = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    new_pattern = ''
    for i in range(len(pattern)):
        new_pattern = new_pattern + base[pattern[-i-1]]
    return new_pattern

def FreqWordsWithRC(seq, length, mismatch):
    # make neighbors
    neighbors = []
    for i in range(len(seq)-length+1):
        pattern = seq[i:i+length]
        neighbors.append(pattern)
    neighbors = Neighbors(neighbors, mismatch)

    # count frequency
    freq_dict={}
    for pattern in neighbors:
        freq = 0
        for i in range(len(seq)-length+1):
            target = seq[i:i+length]
            # freq += HammingCount(target, pattern, mismatch)
            if HammDist(target, pattern) <= mismatch:
                freq += 1
            if HammDist(target, ReverseComplement(pattern)) <= mismatch:
                freq += 1
        freq_dict.update({pattern:freq})
    max_val = max(freq_dict.values())
    max_keys = [k for k, v in freq_dict.items() if v == max_val]
    return ' '.join(max_keys)

print(FreqWordsWithRC(seq, length, mismatch))