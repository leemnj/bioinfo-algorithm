# BA4D: Counting Peptides w/ Given Mass Problem
def CountPeptidesWithMass(target_mass):
    amino_acid_mass = [
        57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
        128, 129, 131, 137, 147, 156, 163, 186
    ]
    
    dp = [0] * (target_mass + 1)
    dp[0] = 1
    
    for mass in range(1, target_mass + 1):
        for aa_mass in amino_acid_mass:
            if mass - aa_mass >= 0:
                dp[mass] += dp[mass - aa_mass]
                
    return dp[target_mass]

# --- main ---
try:
    with open("input/rosalind_ba4d.txt") as f:
        target_mass = int(f.read().strip())
except:
    target_mass = 1201
result = CountPeptidesWithMass(target_mass)
print(result)