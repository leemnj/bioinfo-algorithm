# BA2F: RandomizedMotifSearch

import random as r

def score(motifs):
    t = len(motifs)
    k = len(motifs[0])
    total = 0
    for j in range(k):
        column = [m[j] for m in motifs]
        max_count = max(column.count('A'),
                        column.count('C'),
                        column.count('G'),
                        column.count('T'))
        total += (t - max_count)
    return total

def profile_from_motifs(motifs):
    t = len(motifs)
    k = len(motifs[0])
    profile = {b: [1]*k for b in "ACGT"}  # pseudocount = 1

    for motif in motifs:
        for j, b in enumerate(motif):
            profile[b][j] += 1

    for b in "ACGT":
        for j in range(k):
            profile[b][j] /= (t + 4)

    return profile

# Profile-most probable k-mer (BA2C)
def most_probable_kmer(text, k, profile):
    max_prob = -1
    best = text[:k]
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        prob = 1
        for j, b in enumerate(kmer):
            prob *= profile[b][j]
        if prob > max_prob:
            max_prob = prob
            best = kmer
    return best

def random_motifs(Dna, k):
    motifs = []
    for dna in Dna:
        start = r.randint(0, len(dna) - k)
        motifs.append(dna[start:start+k])
    return motifs

def RandomizedMotifSearch(Dna, k, t):
    motifs = random_motifs(Dna, k)
    best = motifs

    while True:
        profile = profile_from_motifs(motifs)
        motifs = [most_probable_kmer(dna, k, profile) for dna in Dna]

        if score(motifs) < score(best):
            best = motifs
        else:
            return best

def solve(Dna, k, t, iterations=1000):
    best_global = RandomizedMotifSearch(Dna, k, t)

    for _ in range(iterations):
        new = RandomizedMotifSearch(Dna, k, t)
        if score(new) < score(best_global):
            best_global = new

    return best_global

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba2f.txt") as f:
            data = f.read().strip().split()
        # k = int(data[0].split(' ')[0].strip())
        # t = int(data[0].split(' ')[1].strip())
        k, t = int(data[0]), int(data[1])
        Dna = data[2:]
    except:
        k = 8
        t = 5
        Dna = """CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
TAGTACCGAGACCGAAAGAAGTATACAGGCGT
TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
AATCCACCAGCTCCACGTGCAATGTTGGCCTA""".split("\n")
        
    result = solve(Dna, k, t)
    print("\n".join(result))
