from collections import Counter, defaultdict


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # 1. if s1 is longer than s2, return False
        if len(s1) > len(s2):
            return False

        # 2. build target frequency from s1
        target = Counter(s1)

        # 3. initialize window frequency
        window = defaultdict(int)
        # 4. initialize left pointer
        left = 0
        # 5. move right pointer over s2
        for right in range(len(s2)):
            # add s2[right] to window
            window[s2[right]] += 1
            # if window size is larger than len(s1):
            if right - left + 1 > len(s1):
                # remove s2[left] from window
                window[s2[left]] -= 1
                # if count becomes 0, delete the key
                if window[s2[left]] == 0:
                    del window[s2[left]]
                # move left
                left += 1
            # if window equals target:
            if window == target:
                # return True
                return True

        # 6. return False
        return False


if __name__ == "__main__":
    sol = Solution()

    tests = [
        ("ab", "eidbaooo"),
        ("ab", "eidboaoo"),
        ("adc", "dcda"),
        ("a", "a"),
        ("hello", "ooolleoooleh"),
    ]

    for s1, s2 in tests:
        print((s1, s2), "->", sol.checkInclusion(s1, s2))