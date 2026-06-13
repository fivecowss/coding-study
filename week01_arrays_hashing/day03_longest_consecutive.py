def longest_consecutive(nums):
    num_set = set(nums)
    best = 0

    for x in num_set:
        if x - 1 not in num_set:
            length = 1

            while x + length in num_set:
                length += 1

            best = max(best, length)

    return best

if __name__ == "__main__":
    test_cases = [
        [100, 4, 200, 1, 3, 2],
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        [],
        [1],
        [1, 2, 0, 1],
    ]

    for nums in test_cases:
        print(nums, "->", longest_consecutive(nums))