# BA4K: Linear Peptide Scoring Problem

from collections import Counter

MASS = {
    'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,
    'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,
    'R':156,'Y':163,'W':186
}

def linear_spectrum(pep):
    prefix=[0]
    for aa in pep:
        prefix.append(prefix[-1] + MASS[aa])
    out=[0]
    for i in range(len(pep)):
        for j in range(i+1,len(pep)+1):
            out.append(prefix[j]-prefix[i])
    return Counter(out)

def linear_score(peptide, spectrum):
    theo = linear_spectrum(peptide)
    spec = Counter(spectrum)
    return sum(min(theo[m], spec[m]) for m in theo)


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba4k.txt", "r") as f:
            data = f.read().strip().split()
    except:
        data = """NQEL
0 99 113 114 128 227 257 299 355 356 370 371 484
""".strip().split()
    peptide=data[0]
    spectrum=list(map(int,data[1:]))

    print(linear_score(peptide, spectrum))
