# BA4H: Spectral Convolution Problem

def SpectralConvolution(spectrum):
    from collections import Counter
    convolution = []
    n = len(spectrum)
    for i in range(n):
        for j in range(n):
            if i != j:
                diff = spectrum[j] - spectrum[i]
                if diff > 0:
                    convolution.append(diff)
    return Counter(convolution)


if __name__ == "__main__":
    try:
        with open("input/rosalind_ba4h.txt", "r") as f:
            spectrum = list(map(int, f.read().strip().split()))
    except:
        spectrum = [0, 137, 186, 323]
    
    conv = SpectralConvolution(spectrum)

    # decreasing oreder of values
    sorted_items = sorted(conv.items(), key=lambda x: x[1], reverse=True)

    result = []
    for k, v in sorted_items:
        result.extend([k] * v)

    print(*result)
    with open("output/4h.txt", "w") as f:
        f.write(" ".join(map(str, result)))