from collections import Counter

def is_anagram(s, t):
    if len(s) != len(t):
        return False
    
    count = {}

    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    
    for ch in t:
        if ch not in count:
            return False
        count[ch] -= 1
        if count[ch] < 0:
            return False
        
    return True

def is_anagram_counter(s, t):
    return Counter(s) == Counter(t)

if __name__ == "__main__":
    test_cases = [
        ("anagram", "nagaram"),
        ("rat", "car"),
        ("",""),
        ("a", "ab"),
        ("listen", "silent")
    ]

    for s, t in test_cases:
        print(s,t, is_anagram(s, t), is_anagram_counter(s,t))