try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1m.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = "45 4"
content = content.split()
index, k = int(content[0]), int(content[1])

def NumberToPattern(index, k):
    index_list = {0:'A', 1:'C', 2:'G', 3:'T'}
    seq = ''
    for i in range(k-1, -1, -1):
        val = index // (4**i)
        seq = seq + index_list[val]
        index -= val * 4**i
    return seq

print(NumberToPattern(index, k))