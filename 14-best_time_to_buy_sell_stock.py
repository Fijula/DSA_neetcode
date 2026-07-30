# Best Time to Buy and Sell Stock
# prices[i] is the stock price on day i. Buy on one day and sell on a LATER day to
# maximise profit. Return the max profit, or 0 if no profitable trade exists.
# Example: prices=[10,1,5,6,7,1] -> 6   buy at 1, sell at 7
#          prices=[10,8,7,5,2]   -> 0   prices only fall, so do not trade


# Case 1: Brute force: try every buy day against every later sell day
def max_profit_brute(prices):
    best = 0
    n = len(prices)
    for buy in range(n):
        for sell in range(buy + 1, n):
            best = max(best, prices[sell] - prices[buy])
    return best
# Time:  O(n^2)
# Space: O(1)


# Case 2: Optimal: one pass, remember the cheapest price seen so far
def max_profit(prices):
    if not prices:
        return 0

    cheapest = prices[0]               # best price to have bought at, so far
    best = 0
    for price in prices[1:]:
        best = max(best, price - cheapest)   # sell today against the cheapest past day
        cheapest = min(cheapest, price)      # or treat today as the new buy day
    return best
# Time:  O(n)   single pass
# Space: O(1)
# The "buy before sell" rule is respected for free: `cheapest` only ever holds prices
# from days already visited, so it is always strictly before today.


# Case 3: Sliding window phrasing: left = buy day, right = sell day
def max_profit_window(prices):
    left, right = 0, 1
    best = 0
    while right < len(prices):
        if prices[left] < prices[right]:
            best = max(best, prices[right] - prices[left])
        else:
            left = right               # found a cheaper day: move the buy day here
        right += 1
    return best
# Time: O(n), Space: O(1)   the same algorithm, written as a window


if __name__ == "__main__":
    cases = [
        ([10, 1, 5, 6, 7, 1], 6),
        ([10, 8, 7, 5, 2], 0),
        ([7, 1, 5, 3, 6, 4], 5),
        ([], 0),
        ([5], 0),                      # cannot buy and sell on the same day
        ([2, 4, 1], 2),
    ]
    for prices, expected in cases:
        got = max_profit(prices)
        print(prices, "->", got, got == expected)

    print(max_profit_brute([7, 1, 5, 3, 6, 4]))    # 5
    print(max_profit_window([10, 1, 5, 6, 7, 1]))  # 6
