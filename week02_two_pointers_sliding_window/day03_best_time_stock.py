from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # 1. initialize min_price
        min_price = float("inf")
        # 2. initialize best profit
        best_profit = 0

        # 3. loop over prices
        for price in prices:
            # update min_price
            min_price = min(min_price, price)
            # compute current profit
            current_profit = price - min_price
            # update best
            best_profit = max(best_profit, current_profit)

        # 4. return best
        return best_profit


if __name__ == "__main__":
    sol = Solution()

    tests = [
        [7, 1, 5, 3, 6, 4],
        [7, 6, 4, 3, 1],
        [1, 2],
        [2, 1, 2, 1, 0, 1, 2],
    ]

    for prices in tests:
        print(prices, "->", sol.maxProfit(prices))