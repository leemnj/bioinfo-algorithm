try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1n.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = """ACG
1
"""
content = content.split()
pattern = content[0]
d = int(content[1])

def Neighbors(patterns, mismatch):
    '''same as ba1i_subset'''
    neighbor = set()
    for _ in range(mismatch):
        # for pattern in patterns:
        for i in range(len(pattern)):        
            for j in ['A', 'T', 'C', 'G']:
                new_pattern = pattern[:i]+j+pattern[i+1:]
                neighbor.add(new_pattern)
        patterns = list(neighbor)
    neighbor = list(set(neighbor))
    return '\n'.join(neighbor)

print(Neighbors(pattern, d))
    