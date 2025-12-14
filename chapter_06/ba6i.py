# BA6I: Implement GraphToGenome

def ParseEdges(edges_str):
    """
    문자열 형식의 edges를 파싱하여 튜플 리스트로 변환
    예: "(2, 4), (3, 6)" -> [(2, 4), (3, 6)]
    """
    edges = []
    # 괄호를 제거하고 ", " 기준으로 split
    edges_str = edges_str.strip()
    # ), ( 패턴을 찾아서 edge 분리
    edge_strings = edges_str.replace("(", "").replace(")", "").split(", ")
    
    for i in range(0, len(edge_strings), 2):
        u = int(edge_strings[i])
        v = int(edge_strings[i+1])
        edges.append((u, v))
    
    return edges

def IntToNode(i):
    """정수를 노드로 변환"""
    if i % 2 == 0:
        return i // 2
    else:
        return -(i + 1) // 2

def EdgeToGraph(edges):
    """
    edges를 graph (노드 쌍의 리스트)로 변환
    head를 from_node로, tail의 역수를 to_node로 변환하여 cycle 구성
    """
    graph = []
    
    for head, tail in edges:
        from_node = IntToNode(head)
        # tail을 역으로 변환 (2k -> -k, 2k-1 -> k)
        to_node = -IntToNode(tail)
        graph.append((from_node, to_node))
    
    return graph

def GraphToGenome(graph):
    """
    graph (edge 리스트)에서 cycle을 찾아 genome 형식으로 반환
    각 cycle이 하나의 chromosome을 나타냄
    """
    # 인접 리스트 구성
    graph_dict = {}
    all_nodes = set()
    
    for from_node, to_node in graph:
        graph_dict[from_node] = to_node
        all_nodes.add(from_node)
        all_nodes.add(to_node)
    
    visited = set()
    chromosomes = []
    
    # 각 노드에서 시작하여 cycle 찾기
    for start_node in sorted(all_nodes):
        if start_node in visited:
            continue
        
        # 현재 노드에서 시작하여 cycle 따라가기
        chromosome = []
        current = start_node
        
        while current not in visited:
            visited.add(current)
            chromosome.append(current)
            
            # 다음 노드 찾기
            if current in graph_dict:
                current = graph_dict[current]
            else:
                break
        
        if chromosome:
            # 각 cycle에서 절댓값이 가장 작은 노드를 찾아 그 위치에서 시작하도록 정렬
            min_idx = min(range(len(chromosome)), key=lambda i: abs(chromosome[i]))
            rotated_chromosome = chromosome[min_idx:] + chromosome[:min_idx]
            chromosomes.append(tuple(rotated_chromosome))
    
    # chromosome들을 첫 번째 노드의 절댓값으로 정렬
    chromosomes.sort(key=lambda c: abs(c[0]))
    
    return chromosomes

    



if __name__ == "__main__":
    try:
        with open("input/rosalind_ba6i.txt", "r") as f:
            edges_str = f.read().strip()
    except:
        edges_str = "(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)"
    edges = ParseEdges(edges_str)
    graph = EdgeToGraph(edges)
    
    chromosomes = GraphToGenome(graph)
    
    # 양수에 + 붙여서 표기
    # print("Genome: ", end="")
    formatted = []
    for chrom in chromosomes:
        formatted_chrom = "(" + " ".join(f"+{node}" if node > 0 else str(node) for node in chrom) + ")"
        formatted.append(formatted_chrom)
    print("".join(formatted))