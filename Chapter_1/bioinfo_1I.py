try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1i.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''ACGTTGCATGTCGCATGATGCATGAGAGCT
4 1
'''
content = content.split()
seq, length, mismatch = content
length, mismatch = int(length), int(mismatch)

def MakeSubset(patterns, mismatch):
    subset = set()
    for _ in range(mismatch):
        for pattern in patterns:
            for i in range(len(pattern)):        
                for j in ['A', 'T', 'C', 'G']:
                    new_pattern = pattern[:i]+j+pattern[i+1:]
                    subset.add(new_pattern)
        patterns = list(subset)
    subset = list(set(subset))
    return subset

# print(MakeSubset(['ATG'], 1))

def HammingCount(target, pattern, mismatch):
    cnt = 0
    for i in range(len(target)):
        if target[i] != pattern[i]: cnt += 1
    if cnt > mismatch: return 0
    else: return 1

def FreqWords(seq, length, mismatch):
    # make subset first
    patterns = []
    for i in range(len(seq)-length+1):
        pattern = seq[i:i+length]
        patterns.append(pattern)
    patterns = MakeSubset(patterns, mismatch)

    # return patterns
    
    # count frequency
    freq_dict={}
    for pattern in patterns:
        freq = 0
        for i in range(len(seq)-length+1):
            target = seq[i:i+length]
            freq += HammingCount(target, pattern, mismatch)
        freq_dict.update({pattern:freq})
    # print("Total patterns counted:", len(freq_dict))
    max_val = max(freq_dict.values())
    max_keys = [k for k, v in freq_dict.items() if v == max_val]
    # sorted_items = sorted(freq_dict.items(), key = lambda x:x[1], reverse = True)
    # return sorted_items
    return ' '.join(max_keys)
print(FreqWords(seq, length, mismatch))
# print(len(FreqWords(seq, length, mismatch)))