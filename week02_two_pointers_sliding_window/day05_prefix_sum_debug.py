def debug_subarray_sum(nums, k):
    count = {0: 1}
    cur = 0
    ans = 0

    print(f"nums = {nums}, k = {k}")
    print(f"initial: cur={cur}, ans={ans}, count={count}")

    for i, x in enumerate(nums):
        print(f"\nIndex {i}, x = {x}")

        cur += x
        needed = cur - k
        found = count.get(needed, 0)

        print(f"cur = {cur}")
        print(f"needed = cur - k = {cur} - {k} = {needed}")
        print(f"count.get({needed}, 0) = {found}")

        ans += found
        print(f"ans = {ans}")

        count[cur] = count.get(cur, 0) + 1
        print(f"updated count = {count}")

    print(f"\nfinal answer = {ans}")
    return ans


if __name__ == "__main__":
    debug_subarray_sum([1, -1, 1, -1, 1], 0)