def two_sum(nums, target):
    pos = {}

    for i, num in enumerate(nums):
        need = target - num

        if need in pos:
            return [pos[need], i]
        
        pos[num] = i

    return []

if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),
        ([1, 5, 2, 8], 10),
    ]

    for nums, target in test_cases:
        print(nums, target, "->", two_sum(nums, target))