# BA2E: GreedyMotifSearch w. Pseudocounts

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
    '''apply pseudocount'''
    # profile = {b: [0]*k for b in "ACGT"}
    profile = {b: [1/t]*k for b in "ACGT"}

    for motif in motifs:
        for j, b in enumerate(motif):
            profile[b][j] += 1/t

    return profile

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

def GreedyMotifSearch(Dna, k, t):
    first = Dna[0]
    best_motifs = [dna[:k] for dna in Dna]  # 초기값: 각 DNA의 첫 k-mer

    # 첫 DNA의 모든 k-mer를 시작점으로 시도
    for i in range(len(first) - k + 1):
        motifs = [first[i:i+k]]

        # 두 번째 DNA부터 greedy 확장
        for j in range(1, t):
            profile = profile_from_motifs(motifs)
            next_motif = most_probable_kmer(Dna[j], k, profile)
            motifs.append(next_motif)

        # score 비교 후 best 업데이트
        if score(motifs) < score(best_motifs):
            best_motifs = motifs

    return best_motifs

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba2e.txt") as f:
            lines = f.read().strip().split('\n')
            data = [x for x in lines if x.strip() != ""]

        k, t = int(data[0].split(' ')[0].strip()), int(data[0].split(' ')[1].strip())
        DNAs = data[1:]
    except:
        k, t = 3, 5
        DNAs = """GGCGTTCAGGCA
AAGAATCAGTCA
CAAGGAGTTCGC
CACGTCAATCAC
CAATAATATTCG""".split('\n')
    
    print(*GreedyMotifSearch(DNAs, k, t), sep="\n")