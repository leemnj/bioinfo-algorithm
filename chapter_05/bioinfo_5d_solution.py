try:
    with open("sChapter_5/rosalind_ba5d.txt", "r") as f:
        a = f.read()
except FileNotFoundError:
    a = '''0
4
0->1:7
0->2:4
2->3:2
1->4:1
3->4:3'''

a = a.split('\n')
SOURCE = int(a[0])
SINK = int(a[1])
# FROM -> TO : MARK
FROM = [int(n.split('->')[0]) for n in a[2:] if n != '']
AUX = [n.split('->')[1] for n in a[2:] if n != '']
TO = [int(n.split(':')[0]) for n in AUX]
MARK = [int(n.split(':')[1]) for n in AUX]

GRAPH = sorted(zip(FROM,TO,MARK))
print(GRAPH)

def LongestPath(Graph,source,sink):
    '''
    recall:
    GRAPH[i][0] = FROM
    GRAPH[i][1] = TO
    GRAPH[i][2] = MARK
    '''
    s = {}
    path = {}
    for i in range(len(Graph)):
        s[Graph[i][0]] = -float('inf')
        s[Graph[i][1]] = -float('inf')
    s[source] = 0
    for i in range(len(Graph)):
        if s[Graph[i][1]] < s[Graph[i][0]] + Graph[i][2]:
            s[Graph[i][1]] = s[Graph[i][0]] + Graph[i][2]
            path[Graph[i][1]] = Graph[i][0]
    Stack = [sink]
    Stack.append(path[sink])
    while Stack[-1] != source:
        Stack.append(path[Stack[-1]])
    return [s[sink],Stack[::-1]]

Solution = LongestPath(GRAPH,SOURCE,SINK)

for i in range(len(Solution)):
    if i == 0:
        print (Solution[i]) # length
    else:
        print ('->'.join(map(str,Solution[i]))) # path