from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            # 1. compute current sum
            total = numbers[left] + numbers[right]

            # 2. if total == target, return 1-indexed positions
            if total == target:
                return [left + 1, right + 1]

            # 3. if total < target, move left
            if total < target:
                left += 1

            # 4. if total > target, move right
            if total > target:
                right -= 1

        return []


if __name__ == "__main__":
    sol = Solution()

    tests = [
        ([2, 7, 11, 15], 9),
        ([2, 3, 4], 6),
        ([-1, 0], -1),
    ]

    for numbers, target in tests:
        print(numbers, target, "->", sol.twoSum(numbers, target))