from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []

        # 1. sort nums
        nums.sort()

        # 2. loop over nums with index i
        #    i will be the fixed first number
        for i in range(len(nums)):

            # 3. skip duplicate fixed values
            if  i > 0 and nums[i] == nums[i - 1]:
                continue

            # 4. set left and right pointers
            left = i + 1
            right = len(nums) - 1
            # 5. while left < right:
            while left < right:
                # compute total
                total = nums[i] + nums[left] + nums[right]

                # if total == 0:
                if total == 0:
                    # append triplet
                    # move left and right
                    # skip duplicate left values
                    # skip duplicate right values
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

                # elif total < 0:
                    # move left
                elif total < 0:
                    left += 1

                # else:
                    # move right
                else:
                    right -= 1

        return result


if __name__ == "__main__":
    sol = Solution()

    tests = [
        [-1, 0, 1, 2, -1, -4],
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 0, 0],
        [-2, 0, 1, 1, 2],
    ]

    for nums in tests:
        print(nums, "->", sol.threeSum(nums))