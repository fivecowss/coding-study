from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        best = 0

        while left < right:
            # 1. compute width
            width = right - left

            # 2. compute current height
            current_height = min(height[left], height[right])

            # 3. compute area
            area = width * current_height
            # 4. update best
            best = max(best, area)
            # 5. move the pointer with smaller height
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return best


if __name__ == "__main__":
    sol = Solution()

    tests = [
        [1,8,6,2,5,4,8,3,7],
        [1,1],
        [4,3,2,1,4],
        [1,2,1],
    ]

    for height in tests:
        print(height, "->", sol.maxArea(height))