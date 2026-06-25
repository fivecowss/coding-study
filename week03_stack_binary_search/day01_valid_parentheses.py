class Solution:    
    def is_valid(s: str) -> bool:
        stack = []

        pairs = {
            ")": "(",
            "]": "[",
            "}": "{",
        }

        for ch in s:
            if ch in pairs:
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)

        return len(stack) == 0

    if __name__ == "__main__":
        print(is_valid("()"))        # True
        print(is_valid("()[]{}"))    # True
        print(is_valid("(]"))        # False
        print(is_valid("([)]"))      # False
        print(is_valid("{[]}"))      # True