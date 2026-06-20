class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 1. initialize left pointer
        left = 0
        # 2. initialize seen set
        seen = set()
        # 3. initialize best answer
        best = 0

        # 4. move right pointer using for loop
        for right in range(len(s)):
            # 5. while current character is already in seen:
            while s[right] in seen:
                # remove s[left]
                seen.remove(s[left])
                # move left
                left += 1

            # 6. add current character
            seen.add(s[right])

            # 7. update best
            best = max(best, right - left + 1)

        # 8. return best
        return best


if __name__ == "__main__":
    sol = Solution()

    tests = [
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        "",
        " ",
        "dvdf",
        "abba",
    ]

    for s in tests:
        print(repr(s), "->", sol.lengthOfLongestSubstring(s))