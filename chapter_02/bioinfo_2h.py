# BA2H: Distance between Pattern and Strings

def HammingDistance(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

def DistanceBetweenPatternAndStrings(pattern, strings):
    k = len(pattern)
    total_distance = 0
    for string in strings:
        min_distance = float('inf')
        for i in range(len(string) - k + 1):
            kmer = string[i:i + k]
            distance = HammingDistance(pattern, kmer)
            if distance < min_distance:
                min_distance = distance
        total_distance += min_distance
    return total_distance

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba2h.txt", "r") as f:
            data = f.read().strip().splitlines()
            
    except:
        data = """AAA
TTACCTTAAC GATATCTGTC ACGGCGTTCG CCCTAAAGAG CGTCAGAGGT""".splitlines()
    pattern = data[0]
    strings = data[1].split()
    print(DistanceBetweenPatternAndStrings(pattern, strings))