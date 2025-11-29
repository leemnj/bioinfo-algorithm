# BA4C: Generate the Theoretical Spectrum of a Cyclic Peptide

def CyclicSpectrum(peptide):
    prefix_mass = [0]
    amino_acid_mass = {
        'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99,
        'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
        'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131,
        'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186
    }
    
    for i in range(len(peptide)):
        aa = peptide[i]
        prefix_mass.append(prefix_mass[i] + amino_acid_mass[aa])
    
    peptide_mass = prefix_mass[-1]
    cyclic_spectrum = [0]
    
    for i in range(len(peptide)):
        for j in range(i+1, len(peptide)+1):
            cyclic_spectrum.append(prefix_mass[j] - prefix_mass[i])
            if i > 0 and j < len(peptide):
                cyclic_spectrum.append(peptide_mass - (prefix_mass[j] - prefix_mass[i]))
    
    return sorted(cyclic_spectrum)

try:
    with open("input/rosalind_ba4c.txt") as f:
        peptide = f.read().strip()
except:
    peptide = "LEQN"
spectrum = CyclicSpectrum(peptide)
print(' '.join(map(str, spectrum)))
with open("output/4C.txt", "w") as f:
    f.write(' '.join(map(str, spectrum)))