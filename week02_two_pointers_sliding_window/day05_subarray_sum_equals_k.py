from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        # 1. initialize count with {0: 1}
        count = {0: 1}
        # 2. initialize current prefix sum
        cur = 0
        # 3. initialize answer
        ans = 0
        # 4. loop over nums
        for num in nums:
            # update current prefix sum
            cur += num
            # find how many previous prefix sums equal current_sum - k
            prev = cur - k
            # add that number to answer
            ans += count.get(prev, 0)

            # record current prefix sum
            count[cur] = count.get(cur, 0) + 1

        # 5. return answer
        return ans


if __name__ == "__main__":
    sol = Solution()

    tests = [
        ([1, 1, 1], 2),
        ([1, 2, 3], 3),
        ([1, -1, 1, -1, 1], 0),
        ([3], 3),
        ([0, 0, 0], 0),
        ([-1, -1, 1], 0),
    ]

    for nums, k in tests:
        print((nums, k), "->", sol.subarraySum(nums, k))