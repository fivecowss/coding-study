from collections import defaultdict

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # 1. initialize left pointer
        left = 0
        # 2. initialize count dict
        count = defaultdict(int)
        # 3. initialize best answer
        best = 0
        max_freq = 0

        # 4. move right pointer using for loop
        for right in range(len(s)):
            # 5. add current character
            count[s[right]] += 1
            max_freq = max(max_freq, count[s[right]])

            # 6. while current window is invalid:
            while (right - left + 1) - max_freq > k:
                # remove s[left]
                count[s[left]] -= 1
                # move left
                left += 1

            # 7. update best
            best = max(best, right - left + 1)
        
        # 8. return best
        return best
    
if __name__ == "__main__":
        sol = Solution()

        tests = [
            ("ABAB", 2),
            ("AABABBA", 1),
            ("AAAA", 2),
            ("ABCDE", 1),
            ("BAAA", 0),
        ]

        for s, k in tests:
            print((s, k), "->", sol.characterReplacement(s, k))