from bioinfo_1A import PatternCount

def FindClumps(text, k, t):
    Patterns = {}
    for i in range(len(text) - k + 1):
        pattern = text[i:i+k]
        count = PatternCount(text, pattern)
        Patterns.update({pattern : count})
    # FreqPatterns = [k for k, v in Patterns.items() if v == max(Patterns.values())]
    FreqPatterns = [k for k, v in Patterns.items() if v >= t]
    return FreqPatterns
    # return Patterns

input = '''CGGACTCGACAGATGTGAAGAAATGTGAAGACTGAGTGAAGAGAAGAGGAAACACGACACGACATTGCGACATAATGTACGAATGTAATGTGCCTATGGC
5 75 4'''.split()
text = input[0]
k, t = int(input[1]), int(input[3])

# print(FindClumps(text, k, t))

for clump in FindClumps(text, k, t):
    print(clump, end = ' ')