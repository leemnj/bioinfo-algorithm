# BA7B: Limb Length
def limb_length(D, j):
    n = len(D)
    limb = float("inf")

    for i in range(n):
        if i == j:
            continue
        for k in range(n):
            if k == j or k == i:
                continue
            val = (D[i][j] + D[j][k] - D[i][k]) // 2
            limb = min(limb, val)

    return limb

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba7b.txt", "r") as f:
            data = f.read().strip().split('\n')
            n = int(data[0])
            j = int(data[1])
            D = []
            for idx in range(n):
                row = list(map(int, data[2 + idx].split()))
                D.append(row)
    except:
        n = 4
        j = 1
        D = [[0, 13, 21, 22],
             [13, 0, 12, 13],
             [21, 12, 0, 13],
             [22, 13, 13, 0]]
    print(limb_length(D, j))