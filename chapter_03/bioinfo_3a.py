# BA3A: k-mer Composition of a String

def KmerComposition(text, k):
    composition = []
    for i in range(len(text) - k + 1):
        kmer = text[i:i + k]
        composition.append(kmer)
    return sorted(composition)

if __name__ == "__main__":
    try:
        with open("inputs/rosalind_ba3a.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = """5
        CAATCCAAC""".splitlines()
    k = int(data[0])
    string = data[1].strip()
    result = KmerComposition(string, k)
    print('\n'.join(result))