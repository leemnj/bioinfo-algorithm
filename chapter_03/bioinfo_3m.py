# BA3M: Generate All Maximal Non-Branching Paths in a Graph
from textwrap import dedent
def BuildGraph(adj_lines):
    """
    adj_lines: ["1 -> 2,3", "2 -> 4", ...] 형태의 문자열 리스트
    return: graph (dict), indegree, outdegree
    """
    from collections import defaultdict
    
    graph = defaultdict(list)
    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    
    for line in adj_lines:
        line = line.strip()
        if not line:
            continue
        left, right = line.split("->")
        v = left.strip()
        targets = [x.strip() for x in right.strip().split(",")]
        for w in targets:
            graph[v].append(w)
            outdeg[v] += 1
            indeg[w] += 1
            # 노드만 있고 out이 없는 경우도 대비해서 미리 key 확보
            if w not in graph:
                graph[w] = graph[w]  # touch
    
    # 모든 노드에 대해 indeg/outdeg 기본값 0 보장
    for v in list(graph.keys()):
        indeg[v] = indeg.get(v, 0)
        outdeg[v] = outdeg.get(v, 0)
    
    return graph, indeg, outdeg


def is_one_in_one_out(v, indeg, outdeg):
    return indeg[v] == 1 and outdeg[v] == 1


def MaximalNonbranchingPaths(graph, indeg, outdeg):
    """
    graph: dict[node] -> list[neighbor]
    indeg, outdeg: dict[node] -> int
    return: list of paths, each path is a list of nodes (e.g. ["1","2","3"])
    """
    paths = []
    used_edges = set()  # (u, v) 튜플
    
    # 1) non-branching path들 생성
    for v in graph.keys():
        if not is_one_in_one_out(v, indeg, outdeg):
            if outdeg[v] > 0:
                for w in graph[v]:
                    if (v, w) in used_edges:
                        continue
                    path = [v, w]
                    used_edges.add((v, w))
                    # w가 1-in-1-out이면 쭉 extension
                    while is_one_in_one_out(path[-1], indeg, outdeg):
                        curr = path[-1]
                        # curr에서 나가는 edge는 정확히 하나
                        next_node = graph[curr][0]
                        if (curr, next_node) in used_edges:
                            # 이미 사용한 edge라면 더 이상 확장 불가
                            break
                        used_edges.add((curr, next_node))
                        path.append(next_node)
                    paths.append(path)
    
    # 2) isolated cycle들 찾기
    for v in graph.keys():
        if is_one_in_one_out(v, indeg, outdeg):
            # 이 노드에서 나가는 edge 중 아직 안 쓴 게 있다면 cycle 시작
            for w in graph[v]:
                if (v, w) not in used_edges:
                    cycle = [v, w]
                    used_edges.add((v, w))
                    curr = w
                    while True:
                        # curr도 1-in-1-out이어야 isolated cycle 안에 있음
                        if not is_one_in_one_out(curr, indeg, outdeg):
                            break
                        nxt = graph[curr][0]
                        if (curr, nxt) in used_edges:
                            # 이미 돌아온 cycle이거나 사용된 edge면 중단
                            break
                        used_edges.add((curr, nxt))
                        cycle.append(nxt)
                        curr = nxt
                        if curr == v:
                            break
                    # 진짜 cycle인지 확인 (시작점으로 돌아왔는지)
                    if len(cycle) > 1 and cycle[0] == cycle[-1]:
                        paths.append(cycle)
    
    return paths


if __name__ == "__main__":
    import sys
    try:
        with open("input/rosalind_ba3m.txt", "r") as f:
            data = f.read().strip().splitlines()
    except:
        data = dedent("""
                    1 -> 2
                    2 -> 3
                    3 -> 4,5
                    6 -> 7
                    7 -> 6""").strip().splitlines()
    
    graph, indeg, outdeg = BuildGraph(data)
    paths = MaximalNonbranchingPaths(graph, indeg, outdeg)
    
    # 출력 형식 맞추기
    output_lines = []
    for path in paths:
        output_lines.append(" -> ".join(path))
    
    output_str = "\n".join(output_lines)
    print(output_str)
    with open("output/3M.txt", "w") as f:
        f.write(output_str)