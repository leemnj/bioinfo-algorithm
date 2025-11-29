# BA2B: Find a Median String
from itertools import product

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def median_string(k, Dna):
    best_score = float('inf')
    best_pattern = None

    # 모든 4^k k-mer 생성
    for p in product("ACGT", repeat=k):
        pattern = "".join(p)

        # d(Pattern, Dna) 계산
        total_dist = 0
        for text in Dna:
            # d(Pattern, Text)
            min_d = float('inf')
            for i in range(len(text) - k + 1):
                d = hamming(pattern, text[i:i+k])
                if d < min_d:
                    min_d = d
            total_dist += min_d
        
        # 최솟값 갱신
        if total_dist < best_score:
            best_score = total_dist
            best_pattern = pattern

    return best_pattern


# ---------- main ----------
if __name__ == "__main__":
    try:
        with open("./inputs/rosalind_ba2b.txt") as f:
            data = f.read().strip().split()
        k = int(data[0])
        Dna = data[1:]
    except:
        # sample
        k = 3
        Dna = [
            "AAATTGACGCAT",
            "GACGACCACGTT",
            "CGTCAGCGCCTG",
            "GCTGAGCACCGG",
            "AGTACGGGACAG"
        ]

    print(median_string(k, Dna))