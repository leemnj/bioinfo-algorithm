def Limb(D, j):
    """
    리프 j의 LimbLength 계산
    """
    n = len(D)
    min_limb = float('inf')
    
    for i in range(n):
        if i == j:
            continue
        for k in range(n):
            if k == j or k == i:
                continue
            limb_length = (D[i][j] + D[j][k] - D[i][k]) / 2.0
            min_limb = min(min_limb, limb_length)
    
    return min_limb


def find_path(adj, start, end, n_leaves):
    """
    인접 리스트에서 start에서 end까지의 경로 찾기
    """
    from collections import deque
    
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)
    
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        
        if node in adj:
            for neighbor, weight in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
    
    return []


def AdditivePhylogeny(D, n, next_node_id=None):
    """
    가법 계통도 문제를 해결하는 재귀적 알고리즘
    """
    if next_node_id is None:
        next_node_id = n
    
    if n == 2:
        # 베이스 케이스
        adj = {}
        adj[0] = [(1, D[0][1])]
        adj[1] = [(0, D[0][1])]
        return adj, next_node_id
    
    # Limb length 계산
    limb_length = Limb(D, n - 1)
    
    # D의 마지막 행과 열 조정
    D_new = [row[:] for row in D]
    for j in range(n - 1):
        D_new[j][n - 1] = D[j][n - 1] - limb_length
        D_new[n - 1][j] = D[n - 1][j] - limb_length
    
    # 조건 Di,k = Di,n + Dn,k을 만족하는 i와 k 찾기
    i, k = None, None
    for ii in range(n - 1):
        for kk in range(n - 1):
            if ii != kk:
                if abs(D_new[ii][kk] - (D_new[ii][n-1] + D_new[n-1][kk])) < 1e-9:
                    i, k = ii, kk
                    break
        if i is not None:
            break
    
    if i is None:
        i, k = 0, 1
    
    x = D_new[i][n - 1]
    
    # D에서 마지막 행과 열 제거
    D_reduced = [row[:-1] for row in D_new[:-1]]
    
    # 재귀적으로 호출
    T, next_node_id = AdditivePhylogeny(D_reduced, n - 1, next_node_id)
    
    # i에서 k로의 경로 찾기
    path = find_path(T, i, k, n - 1)
    
    # 경로상에서 i로부터 거리 x인 노드 찾기
    if path:
        current_dist = 0
        for idx in range(len(path) - 1):
            u = path[idx]
            v = path[idx + 1]
            
            # u에서 v로의 엣지 가중치 찾기
            edge_weight = None
            if u in T:
                for neighbor, weight in T[u]:
                    if neighbor == v:
                        edge_weight = weight
                        break
            
            if edge_weight is not None:
                if current_dist + edge_weight >= x:
                    # 새 내부 노드 생성
                    v_new = next_node_id
                    next_node_id += 1
                    
                    remaining = x - current_dist
                    
                    # 기존 엣지 제거 및 새 노드 추가
                    T[u] = [(neighbor, weight) for neighbor, weight in T[u] if neighbor != v]
                    T[u].append((v_new, remaining))
                    
                    if v not in T:
                        T[v] = []
                    T[v] = [(neighbor, weight) for neighbor, weight in T[v] if neighbor != u]
                    T[v].append((v_new, edge_weight - remaining))
                    
                    # 새로운 노드에서 v로의 엣지
                    T[v_new] = [(u, remaining), (v, edge_weight - remaining)]
                    
                    # 리프 n-1을 v_new에 추가
                    T[v_new].append((n - 1, limb_length))
                    T[n - 1] = [(v_new, limb_length)]
                    
                    return T, next_node_id
                
                current_dist += edge_weight
    
    # 경로가 없거나 찾을 수 없는 경우 (드물게 발생)
    v_new = next_node_id
    next_node_id += 1
    
    if i not in T:
        T[i] = []
    T[i].append((v_new, x))
    
    T[v_new] = [(i, x), (n - 1, limb_length)]
    T[n - 1] = [(v_new, limb_length)]
    
    return T, next_node_id


def read_input(filename):
    """입력 파일 읽기"""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    n = int(lines[0])
    D = []
    for i in range(1, n + 1):
        row = list(map(float, lines[i].split()))
        D.append(row)
    
    return n, D


def print_tree(adj):
    """
    트리를 인접 리스트 형식으로 출력 (정렬된 형식)
    """
    result = []
    for u in sorted(adj.keys()):
        for v, weight in adj[u]:
            result.append(f"{u}->{v}:{int(weight)}")
    return '\n'.join(result)


def read_input(filename):
    """입력 파일 읽기"""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    n = int(lines[0])
    D = []
    for i in range(1, n + 1):
        row = list(map(float, lines[i].split()))
        D.append(row)
    
    return n, D


# 테스트
if __name__ == "__main__":
    import sys
    
    # 입력 파일에서 읽기
    input_file = "input/rosalind_ba7c.txt"
    try:
        n, D = read_input(input_file)
        adj, _ = AdditivePhylogeny(D, n)
        print(print_tree(adj))
    except FileNotFoundError:
        print("use example!")
        # 샘플 테스트
        sample_D = [
            [0, 13, 21, 22],
            [13, 0, 12, 13],
            [21, 12, 0, 13],
            [22, 13, 13, 0]
        ]
        adj, _ = AdditivePhylogeny(sample_D, 4)
        print(print_tree(adj))
