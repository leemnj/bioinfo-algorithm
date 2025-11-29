# BA4B: Find Substrings of a Genome Encoding a Given AA String
from textwrap import dedent

CODON_TABLE = {
    "UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L",
    "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S",
    "UAU":"Y", "UAC":"Y", "UAA":"STOP", "UAG":"STOP",
    "UGU":"C", "UGC":"C", "UGA":"STOP", "UGG":"W",
    "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
    "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M",
    "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T",
    "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K",
    "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R",
    "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
    "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G",
}

def RnaToPtn(rna):
    peptide = []
    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if codon not in CODON_TABLE:
            break
        aa = CODON_TABLE[codon]
        if aa == "STOP":
            break
        peptide.append(aa)
    return "".join(peptide)

def ReverseComplement(dna):
    complement = {'A':'U', 'U':'A', 'C':'G', 'G':'C'}
    rc_dna = ''.join(complement[base] for base in reversed(dna))
    return rc_dna

def FindSubstring(dna, aa):
    length = 3*len(aa)
    substrings = []
    
    rna = dna.replace("T", "U")
    
    for i in range(len(rna)):
        substring = rna[i:i+length]
        peptide = RnaToPtn(substring)
        RCpeptide = RnaToPtn(ReverseComplement(substring))
        if peptide == aa or RCpeptide == aa:
            substrings.append(substring.replace("U", "T"))
    return substrings

# --- main ---
try:
    with open("input/rosalind_ba4b.txt") as f:
        lines = f.readlines()
except:
    lines = dedent("""
                   ATGGCCATGGCCCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA
                   MA""").strip().splitlines()
dna = lines[0].strip()
aa = lines[1].strip()

result = FindSubstring(dna, aa)
print(result)
with open("output/4B.txt", "w") as f:
    f.write("\n".join(result))