# BA2C: Profile-most Probable k-mer

def profile_matrix(profile):
    bases = "ACGT"
    matrix = {}
    for base, line in zip(bases, profile):
        matrix[base] = list(map(float, line.split(' ')))
    return matrix

def most_probable_kmer(text, k, matrix):
    max_score = 0
    probable_kmer = ""

    for i in range(len(text) - k + 1):
        pattern = text[i:i+k]
        score = 1
        for j in range(k):
            score = score * matrix[pattern[j]][j]
        if score > max_score:
            max_score = score
            probable_kmer = pattern

    return probable_kmer

if __name__ == "__main__":
    try:
        with open("./inputs/rosalind_ba2c.txt") as f:
            lines = f.read().strip().split('\n')
            data = [x for x in lines if x.strip() != ""]

        text = data[0]
        k = int(data[1])
        profile = data[2:]
    except:
        text = 'ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT'
        k = 5
        profile = """0.2 0.2 0.3 0.2 0.3
0.4 0.3 0.1 0.5 0.1
0.3 0.3 0.5 0.2 0.4
0.1 0.2 0.1 0.1 0.2""".split('\n')
    
    matrix = profile_matrix(profile)
    print(most_probable_kmer(text, k, matrix))