def contains_duplicate(nums):
    seen = set()

    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    
    return False

def contains_duplicate_v2(nums):
    return len(nums) != len(set(nums))

if __name__ == "__main__":
    test_cases = [
        [1, 2, 3, 1],
        [1, 2, 3, 4],
        [],
        [1],
        [0, 0],
    ]

    for nums in test_cases:
        print(nums, contains_duplicate(nums), contains_duplicate_v2(nums))
        