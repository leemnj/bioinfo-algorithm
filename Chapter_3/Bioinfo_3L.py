# BA3L: Construct a String Spelled by a Gapped Genome Path
from textwrap import dedent

def reconsturct_gapped_spring(kmers, k, d):
    prefix_map = {}
    suffix_map = {}
    
    for kmer in kmers:
        first_part, second_part = kmer.split('|')
        prefix = first_part[:-1] + '|' + second_part[:-1]
        suffix = first_part[1:] + '|' + second_part[1:]
        prefix_map.setdefault(prefix, []).append(suffix)
        suffix_map.setdefault(suffix, []).append(prefix)
    
    start_node = None

    for node in prefix_map:
        out_degree = len(prefix_map[node])
        in_degree = len(suffix_map.get(node, []))
        if out_degree - in_degree == 1:
            start_node = node
            break
    
    if not start_node:
        start_node = kmers[0].split('|')[0][:-1] + '|' + kmers[0].split('|')[1][:-1]
    
    path = [start_node]
    while True:
        current_node = path[-1]
        if current_node in prefix_map and prefix_map[current_node]:
            next_node = prefix_map[current_node].pop()
            path.append(next_node)
        else:
            break
    
    first_string = path[0].split('|')[0]
    second_string = path[0].split('|')[1]
    
    for node in path[1:]:
        first_string += node.split('|')[0][-1]
        second_string += node.split('|')[1][-1]
    
    reconstructed_string = first_string + second_string[-(k + d):]
    
    return reconstructed_string

if __name__ == "__main__":
    try:
        with open("input/rosalind_ba3l.txt", "r") as f:
            data = f.read().strip().splitlines()
            
    except:
        k, d = 4, 2
        data = dedent("""
                    4 2
                    GACC|GCGC
                    ACCG|CGCC
                    CCGA|GCCG
                    CGAG|CCGG
                    GAGC|CGGA""").strip().splitlines()
    k, d = map(int, data[0].split())
    kmers = data[1:]
    result = reconsturct_gapped_spring(kmers, k, d)
    print(result)
    with open("output/3L.txt", "w") as f:
        f.write(result)