# BA4L: Trim Problem

from collections import Counter

# mass table
MASS = {
    'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I':113,'L':113,
    'N':114,'D':115,'K':128,'Q':128,'E':129,'M':131,'H':137,'F':147,
    'R':156,'Y':163,'W':186
}

def linear_spectrum(peptide):
    prefix=[0]
    for aa in peptide: prefix.append(prefix[-1] + MASS[aa])
    out=[0]
    for i in range(len(peptide)):
        for j in range(i+1,len(peptide)+1):
            out.append(prefix[j]-prefix[i])
    return Counter(out)

def LinearScore(peptide, spectrum):
    theo = linear_spectrum(peptide)
    spec = Counter(spectrum)
    return sum(min(theo[v], spec[v]) for v in theo)

def Trim(Leaderboard, Spectrum, N):
    scored=[(p, LinearScore(p, Spectrum)) for p in Leaderboard]
    scored.sort(key=lambda x:x[1], reverse=True)

    # cutoff score = N번째 점수
    cutoff = scored[N-1][1] if len(scored) >= N else scored[-1][1]

    return [p for p,s in scored if s >= cutoff]


# ================= RUN =================
if __name__=="__main__":
    # import sys
    # data=sys.stdin.read().strip().split()
    try:
        with open("input/rosalind_ba4l.txt", "r") as f:
            data = f.read().splitlines()
    except:
        data = """
LAST ALST TLLT TQAS
0 71 87 101 113 158 184 188 259 271 372
2""".strip().splitlines()
    # 첫 줄 = peptides
    Leaderboard=data[0].split()
    Spectrum=list(map(int,data[1].split()))
    N=int(data[2])

    result=Trim(Leaderboard,Spectrum,N)
    print(*result)
