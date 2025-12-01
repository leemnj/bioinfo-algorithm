from collections import Counter

# ===== 1. Convolution Top M 선택 =====
def topMspectrum(M, spectrum):
    conv=[]
    for i in range(len(spectrum)):
        for j in range(len(spectrum)):
            diff=spectrum[j]-spectrum[i]
            if 57<=diff<=200:
                conv.append(diff)

    counts=Counter(conv).most_common()

    if len(counts)<=M:
        return [m for m,_ in counts]

    cutoff=counts[M-1][1]
    return [m for m,c in counts if c>=cutoff]


# ===== 2. Cyclic Spectrum + Cyclic Score =====
def cyclic_spectrum(pep):
    prefix=[0]
    for x in pep: prefix.append(prefix[-1]+x)
    total=prefix[-1]
    out=[0]
    for i in range(len(pep)):
        for j in range(i+1,len(pep)+1):
            m=prefix[j]-prefix[i]
            out.append(m)
            if i>0 and j<len(pep): out.append(total-m)
    return Counter(out)

def score_cyclic(pep, spectrumCounter):
    theo=cyclic_spectrum(pep)
    return sum(min(theo[x], spectrumCounter[x]) for x in theo)


# ===== 3. ConvolutionCyclopeptideSequencing (Cyclic only) =====
def ConvolutionCyclopeptideSeq_CyclicOnly(M, N, spectrum):
    specCount=Counter(spectrum)
    parent=max(spectrum)

    massList = topMspectrum(M, spectrum)  # allowed masses

    leaderboard=[[]]
    leader=[]

    while leaderboard:

        # Expand
        leaderboard=[p+[m] for p in leaderboard for m in massList]
        scored=[]

        for pep in leaderboard:
            mass=sum(pep)

            # 반드시 cyclic score로 평가
            cscore=score_cyclic(pep, specCount)

            if mass==parent:
                # Leader 갱신
                if not leader or cscore>score_cyclic(leader, specCount):
                    leader=pep
                scored.append((pep,cscore))

            elif mass<parent:
                scored.append((pep,cscore))

        if not scored: break

        # leaderboard trim (top N + ties)
        scored.sort(key=lambda x:x[1], reverse=True)
        cutoff=scored[N-1][1] if len(scored)>=N else scored[-1][1]
        leaderboard=[p for p,s in scored if s>=cutoff]

    return leader


# ============ RUN ============

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba4i.txt", "r") as f:
            data = f.read().strip().split()
    except:
        data="""
20
60
57 57 71 99 129 137 170 186 194 208 228 265 285 299 307 323 356 364 394 422 493
""".strip().split()
    M=int(data[0]); N=int(data[1])
    spectrum=list(map(int,data[2:]))

    result=ConvolutionCyclopeptideSeq_CyclicOnly(M,N,spectrum)
    print("-".join(map(str,result)))
