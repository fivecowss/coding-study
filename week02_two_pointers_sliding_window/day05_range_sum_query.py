from typing import List


class NumArray:
    def __init__(self, nums: List[int]):
        # 1. initialize prefix with [0]
        self.prefix = [0]

        # 2. loop over nums
            # append previous prefix sum + current number
        for num in nums:
            prefix_sum = self.prefix[-1] + num
            self.prefix.append(prefix_sum)

        pass

    def sumRange(self, left: int, right: int) -> int:
        # 3. use prefix[right + 1] - prefix[left]
        return self.prefix[right + 1] - self.prefix[left]

if __name__ == "__main__":
    nums = [-2, 0, 3, -5, 2, -1]
    obj = NumArray(nums)

    print(obj.sumRange(0, 2))  # 1
    print(obj.sumRange(2, 5))  # -1
    print(obj.sumRange(0, 5))  # -3