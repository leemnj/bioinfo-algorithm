try:
    with open("Bioinfo algorithm/Chapter_1/rosalind_ba1l.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''AGT'''

content = content.split()[0]

def PatternToNumber(pattern):
    base_dict = {'A':0, 'C':1, 'G':2, 'T':3}
    num = 0
    for char in pattern:
        num += base_dict[char]
        num *= 4
    num /= 4
    return int(num)

if __name__ == "__main__":
    print(PatternToNumber(content))

'''
def patternToNumber (pattern):
letter_value = {'A':0, 'C':1, 'G':2, 'T':3}

total = 0
for i in range(len(pattern)):
    ## grab the letters from the rear ([-(i+1)]) for increasing i's and 
    ## multiply it's value by the position it's in
    total += letter_value[pattern[-(i+1)]] * len(letter_value)**(i)

return total
'''