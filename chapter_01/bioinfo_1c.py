def ReverseComplement(old_pattern):
    dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
    new_pattern = ''
    for i in range(len(old_pattern)):
        new_pattern = new_pattern + dict[old_pattern[-1-i]]
    return new_pattern

pattern = 'AAAACCCGGT'
print(ReverseComplement(pattern))