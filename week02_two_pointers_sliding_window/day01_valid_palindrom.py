class Solution:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            # 1. move left if s[left] is not alphanumeric
            if not s[left].isalnum():
                left += 1
                continue

            # 2. move right if s[right] is not alphanumeric
            if not s[right].isalnum():
                right -= 1
                continue

            # 3. compare lowercase characters
            if s[left].lower() != s[right].lower():
                return False

            # 4. move both pointers inward
            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    sol = Solution()

    tests = [
        "A man, a plan, a canal: Panama",
        "race a car",
        " ",
        "0P"
    ]

    for s in tests:
        print(s, "->", sol.isPalindrome(s))