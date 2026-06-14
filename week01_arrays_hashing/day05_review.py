from collections import Counter, defaultdict

def contains_duplicate(nums):
    seen = set()

    for nums in nums:
        if nums in seen:
            return True
        seen.add(nums)
    return False
    pass

def is_anagram(s, t):
    
    if len(s) != len(t):
        return False
    
    freq = {}
    
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    for ch in t:
        if ch not in freq:
            return False
        freq[ch] -= 1
        if freq[ch] < 0:
            return False
    pass

def two_sum(nums, target):
    pos = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in pos:
            return [pos[need], i]
        
        pos[x] = i
    pass

def group_anagrams(strs):
    groups = defaultdict(list)

    for word in strs:
        key = "".joint(sorted(word))
        groups[key].append(word)

    return list(groups.values())
    pass

def top_k_frequent(nums, k):
    freq = Counter(nums)
    return [num for num, count in freq.most_common(k)]
    pass

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
    pass

def product_except_self(nums):
    prefix = 1
    result = [1] * len(nums)
    for i in range(len(nums)):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result
    pass

def is_valid_sudoku(board):
    pass

if __name__ == "__main__":
    print("Review file")

