# overlap alignment
try:
    with open("Chapter_5/rosalind_ba5i.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''PAWHEAE
HEAGAWGHEE'''

lines = content.split('\n')
v, w = lines[0], lines[1]

def OverlapAlign(v, w):