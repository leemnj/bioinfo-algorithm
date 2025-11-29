# BA4G: Implement LeaderboardCyclopeptideSequencing
AMINO = [57,71,87,97,99,101,103,113,114,115,128,129,131,137,147,156,163,186]

def linear_spec(pep):
    prefix=[0]
    for m in pep: prefix.append(prefix[-1]+m)
    spec=[0]
    for i in range(len(pep)):
        for j in range(i+1,len(pep)+1):
            spec.append(prefix[j]-prefix[i])
    return spec

def cyclic_spec(pep):
    prefix=[0]
    for m in pep: prefix.append(prefix[-1]+m)
    total=prefix[-1]
    spec=[0]
    for i in range(len(pep)):
        for j in range(i+1,len(pep)+1):
            mass=prefix[j]-prefix[i]
            spec.append(mass)
            if i>0 and j<len(pep):
                spec.append(total-mass)
    return spec


def leaderboard_cyclopeptide_sequencing(spec,N):
    from collections import Counter
    target=Counter(spec)
    parent=max(spec)

    leaderboard=[[]]
    leader=[]

    while leaderboard:
        # Expand
        leaderboard=[p+[m] for p in leaderboard for m in AMINO]

        # Score + Prune
        scored=[]
        for pep in leaderboard:
            mass=sum(pep)

            if mass==parent:
                # full peptide -> cyclic scoring only when complete
                theo=Counter(cyclic_spec(pep))
                s=sum(min(theo[x],target[x]) for x in theo)
                if leader==[]:
                    leader=pep
                else:
                    best=sum(min(Counter(cyclic_spec(leader))[x],target[x]) 
                             for x in Counter(cyclic_spec(leader)))
                    if s>best: leader=pep
                scored.append((pep,s))
            elif mass<parent:
                # partial peptide -> linear scoring (much cheaper)
                theo=Counter(linear_spec(pep))
                s=sum(min(theo[x],target[x]) for x in theo)
                scored.append((pep,s))

        if not scored: break

        # sort + Cut (keep best N incl ties)
        scored.sort(key=lambda x:x[1],reverse=True)
        cutoff=scored[N-1][1] if len(scored)>=N else scored[-1][1]
        leaderboard=[p for p,s in scored if s>=cutoff]

    return leader


# ========== RUN ==========
if __name__ == "__main__":
    from textwrap import dedent
    try:
        with open("input/rosalind_ba4g.txt", "r") as f:
            data = f.read().strip().split()
    except:
        data = dedent("""
10
0 71 113 129 147 200 218 260 313 331 347 389 460""").strip().split()
    N=int(data[0])
    spectrum_input=list(map(int,data[1:]))
    # print(N, spectrum_input)
    ans=leaderboard_cyclopeptide_sequencing(spectrum_input,N)
    print("-".join(map(str,ans)))
