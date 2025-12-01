# BA4J: LinearSpectrumProblem

MASS = {
    'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,
    'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,
    'R':156,'Y':163,'W':186
}

def linear_spectrum(peptide):
    prefix=[0]
    for aa in peptide:
        prefix.append(prefix[-1] + MASS[aa])   # prefix mass array 생성
    
    spectrum=[0]
    for i in range(len(peptide)):
        for j in range(i+1,len(peptide)+1):
            spectrum.append(prefix[j] - prefix[i])  # linear fragment mass
    
    return sorted(spectrum)


if __name__=="__main__":
    # import sys
    # peptide=sys.stdin.read().strip()
    try:
        with open("input/rosalind_ba4j.txt", "r") as f:
            peptide = f.read().strip()
    except:
        peptide = "NQEL"
    print(*linear_spectrum(peptide))
