# BA2A: Motif Enumeration

def hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

# Generate all neighbors within <= d mismatches
def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {"A", "C", "G", "T"}
    
    suffix_neighbors = neighbors(pattern[1:], d)
    result = set()
    for text in suffix_neighbors:
        if hamming(pattern[1:], text) < d:
            # mismatch allowed at first position
            for base in "ACGT":
                result.add(base + text)
        else:
            # must match first position
            result.add(pattern[0] + text)
    return result

def motif_enumeration(Dna, k, d):
    patterns = set()

    # 모든 DNA 문자열에서 k-mer를 수집
    kmer_sets = [
        {dna[i:i+k] for i in range(len(dna) - k + 1)}
        for dna in Dna
    ]

    # 첫 번째 문자열의 k-mer만 대상
    for kmer in kmer_sets[0]:

        # 이 kmer의 모든 neighbors 생성
        for nbd in neighbors(kmer, d):
            found_in_all = True
            for s in kmer_sets[1:]:
                # mismatch ≤ d 인 k-mer가 있는지 검사
                if not any(hamming(nbd, x) <= d for x in s):
                    found_in_all = False
                    break

            # 조건 만족하면 motif 패턴에 추가
            if found_in_all:
                patterns.add(nbd)

    return sorted(patterns)


# ---------- main ----------
if __name__ == "__main__":
    try:
        with open("./inputs/rosalind_ba2a.txt") as f:
            data = f.read().strip().split()
        k, d = map(int, data[:2])
        Dna = data[2:]
    except:
        # sample test
        k, d = 3, 1
        Dna = ["ATTTGGC", "TGCCTTA", "CGGTATC", "GAAAATT"]
    
    result = motif_enumeration(Dna, k, d)
    print(" ".join(sorted(result)))
