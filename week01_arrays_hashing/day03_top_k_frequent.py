from collections import Counter

def top_k_frequent(nums, k):
    freq = Counter(nums)

    result = []
    for nums, count in freq.most_common(k):
        result.append(nums)

    return result

def top_k_frequent_v2(nums, k):
    freq = Counter(nums)
    return [num for num, count in freq.most_common(k)]


def top_k_frequent_manual(nums, k):
    freq = {}

    for x in nums:
        freq[x] = freq.get(x, 0) + 1

    sorted_items = sorted(freq.items(), key = lambda x: x[1], reverse = True)
    
    result = []
    for nums, count in sorted_items[:k]:
        result.append(nums)

    return result


if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2),
        ([1], 1),
        ([4, 4, 4, 6, 6, 7], 2),
        ([5, 3, 5, 2, 3, 5, 2, 2], 2),
    ]

    for nums, k in test_cases:
        print(nums, k, "->", top_k_frequent(nums, k))
        print("v2:", top_k_frequent_v2(nums, k))
        print("manual:", top_k_frequent_manual(nums, k))
