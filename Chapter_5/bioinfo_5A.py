try:
    with open("Bioinfo algorithm/Chapter_5/rosalind_ba5a.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    content = '''40
1,5,10,20,25,50
'''

content = content.split('\n')
# print(content)
money = int(content[0])
coins = list(map(int, content[1].split(',')))

def min_coin_change(money, coins):
    dp = [float('inf')] * (money + 1)
    dp[0] = 0

    for m in range(1, money + 1):
        for coin in coins:
            if m - coin >= 0:
                dp[m] = min(dp[m], dp[m-coin] + 1)
    return dp[money]

print(min_coin_change(money, coins))