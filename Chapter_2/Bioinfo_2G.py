# BA2G: Gibbs Sampler
'''
the iteration number is too small so I change N=2000 to 5000 to solve this problem.
'''
import random as r

def profile(motifs, psuedocounts=1):
    k = len(motifs[0])
    profile = {'A':[psuedocounts]*k, 'C':[psuedocounts]*k, 'G':[psuedocounts]*k, 'T':[psuedocounts]*k}
    for motif in motifs:
        for i in range(k):
            profile[motif[i]][i] += 1
    for nucleotide in profile:
        for i in range(k):
            profile[nucleotide][i] /= (len(motifs) + 4*psuedocounts)
    return profile

def score(motifs):
    k = len(motifs[0])
    score = 0
    for i in range(k):
        count = {'A':0, 'C':0, 'G':0, 'T':0}
        for motif in motifs:
            count[motif[i]] += 1
        max_count = max(count.values())
        score += (len(motifs) - max_count)
    return score

def GibbsSampler(Dna, k, t, N):
    motifs = []
    
    for i in range(t):
        rand_index = r.randint(0, len(Dna[i]) - k)
        motifs.append(Dna[i][rand_index:rand_index + k])
    best_motifs = motifs[:]
    
    for _ in range(N):
        i = r.randint(0, t - 1)
        motifs_except_i = motifs[:i] + motifs[i+1:]
        profile_matrix = profile(motifs_except_i, 1)
        probabilities = []
        for j in range(len(Dna[i]) - k + 1):
            kmer = Dna[i][j:j + k]
            prob = 1
            for m in range(k):
                prob *= profile_matrix[kmer[m]][m]
            probabilities.append(prob)
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]
        rnum = r.random()
        cumulative_prob = 0
        for index, prob in enumerate(probabilities):
            cumulative_prob += prob
            if rnum <= cumulative_prob:
                selected_kmer = Dna[i][index:index + k]
                break
        motifs[i] = selected_kmer
        if score(motifs) < score(best_motifs):
            best_motifs = motifs[:]
    return best_motifs

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba2g.txt", "r") as f:
            data = f.read().strip().split()
            k, t, N = int(data[0]),int(data[1]), int(data[2])
            Dna = data[3:]
    except:
        k, t, N = 8, 5, 100
        Dna = """CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
TAGTACCGAGACCGAAAGAAGTATACAGGCGT
TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
AATCCACCAGCTCCACGTGCAATGTTGGCCTA""".split("\n")
    result = GibbsSampler(Dna, k, t, 5000)
    print("\n".join(result))