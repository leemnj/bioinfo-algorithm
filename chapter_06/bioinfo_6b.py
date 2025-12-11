# BA6B: Number of Breakpoints in a Permutation
def parse_permutation(line: str):
    """
    "(+3 +4 +5 -12 ...)" 형식을 [3, 4, 5, -12, ...] 리스트로 파싱
    """
    line = line.strip()
    line = line.replace("(", "").replace(")", "")
    parts = line.split()
    return [int(x) for x in parts]


def count_breakpoints(P):
    """
    P: signed permutation (list[int])
    return: number of breakpoints
    정의: 0, n+1을 양끝에 붙인 뒤,
          인접한 쌍 (a, b)에 대해 b - a != 1 인 곳의 개수
    """
    n = len(P)
    extended = [0] + P + [n + 1]

    cnt = 0
    for i in range(len(extended) - 1):
        if extended[i + 1] - extended[i] != 1:
            cnt += 1
    return cnt


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba6b.txt", "r") as f:
            line = f.readline()
    except: line = "(+3 +4 +5 -12 -8 -7 -6 +1 +2 +10 +9 -11 +13 +14)"
    P = parse_permutation(line)
    print(count_breakpoints(P))