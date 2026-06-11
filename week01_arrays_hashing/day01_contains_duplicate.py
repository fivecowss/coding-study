def contains_duplicate(nums):
    seen = set()

    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    
    return False

if __name__ == "__main__":
    print(contains_duplicate([1,2,3,1]))
    print(contains_duplicate([1, 2, 3, 4]))
    print(contains_duplicate([]))
    print(contains_duplicate([1]))
    