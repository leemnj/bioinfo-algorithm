try:
    with open("Bioinfo algorithm/Chapter_5/rosalind_ba5b.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''4 4
1 0 2 4 3
4 6 5 2 1
4 4 5 2 1
5 6 8 5 3
-
3 2 4 0
3 2 4 2
0 7 3 3
3 3 0 2
1 3 2 2'''

# 줄 단위로 나누기
lines = content.strip().split('\n')

# 첫 줄: m, n
n, m = map(int, lines[0].split())

# --- 구분선 인덱스 찾기
split_idx = lines.index('-')

# 행렬1: 두 번째 줄부터 --- 이전까지
v_matrix = [list(map(int, row.split())) for row in lines[1:split_idx]]

# 행렬2: --- 이후부터 끝까지
h_matrix = [list(map(int, row.split())) for row in lines[split_idx+1:]]

# 확인용 출력
# print("m =", m, "n =", n)
# print("Matrix1 =", matrix1)
# print("Matrix2 =", matrix2)

def ManhattanGrid(n, m, v_mat, h_mat):
    dp = [[0 for j in range(m+1)] for i in range(n+1)]
    for i in range(n):
        dp[i+1][0] = dp[i][0] + v_mat[i][0]
    for j in range(m):
        dp[0][j+1] = dp[0][j] + h_mat[0][j]
    
    for i in range(n):
        for j in range(m):
            dp[i+1][j+1] = max(dp[i][j+1]+v_mat[i][j+1], dp[i+1][j]+h_mat[i+1][j])

    print(dp[n][m])

ManhattanGrid(n, m, v_matrix, h_matrix)

'''
v_mat(vertical) -> down
h_mat(horizontal) -> right
으로 할 껄
'''