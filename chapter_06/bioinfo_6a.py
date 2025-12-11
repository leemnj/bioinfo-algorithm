# BA6A: Implement GreedySorting

def parse_permutation(line: str):
    line = line.strip()
    line = line.replace("(", "").replace(")", "")
    parts = line.split()
    return [int(x) for x in parts]

def format_permutation(perm):
    s = []
    for x in perm:
        if x > 0:
            s.append(f"+{x}")
        else:
            s.append(str(x))
    return "(" + " ".join(s) + ")"

def GreedySort(sequence):
    P = sequence[:]
    n = len(P)
    result = []

    for k in range(n):
        if abs(P[k]) != k + 1:
            # 위치 찾기
            j = None
            for idx in range(k, n):
                if abs(P[idx]) == k + 1:
                    j = idx
                    break

            # reversal + sign flip
            P[k:j+1] = [-x for x in P[k:j+1][::-1]]
            result.append(P[:])

        if P[k] == -(k + 1):
            P[k] = k + 1
            result.append(P[:])

    return result

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba6a.txt", "r") as f:
            line = f.read().strip()
    except:
        line = "(-3 +4 +1 +5 -2)"
    P = parse_permutation(line)
    steps = GreedySort(P)
    result = ""
    for perm in steps:
        result = result + format_permutation(perm) + "\n"
    result = result.strip()
    
    with open("output/6a.txt", "w") as f:
        f.write(result)