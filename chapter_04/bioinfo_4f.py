# BA4F: Compute Score of Cyclic Peptide Against Spectrum

MASS = {
    'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,
    'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,
    'R':156,'Y':163,'W':186
}

def cyclic_spectrum(peptide):
    """Return theoretical cyclic spectrum of peptide as integer mass list."""
    prefix = [0]
    for aa in peptide:
        prefix.append(prefix[-1] + MASS[aa])
    total = prefix[-1]

    spectrum = [0]
    n = len(peptide)

    for i in range(n):
        for j in range(i+1, n+1):
            spectrum.append(prefix[j]-prefix[i])  # linear fragment
            if i > 0 and j < n:                   # wrap-around → cyclic fragment
                spectrum.append(total-(prefix[j]-prefix[i]))

    return sorted(spectrum)


def score(peptide, spectrum):
    """Score(Peptide,Spectrum) = shared mass count with multiplicity."""
    from collections import Counter
    theo = Counter(cyclic_spectrum(peptide))
    exp  = Counter(spectrum)
    return sum(min(theo[m], exp[m]) for m in theo)


# ======== RUN ========
if __name__ == "__main__":
    try:
        with open("input/rosalind_ba4f.txt", "r") as f:
            lines = f.readlines()
    except:
        lines = ["NQEL", "0 99 113 114 128 227 257 299 355 356 370 371 484"]
    
    peptide = lines[0].strip()
    spectrum = list(map(int, lines[1].strip().split()))
    
    result = score(peptide, spectrum)
    print(result)