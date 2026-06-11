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

if __name__ == "__main__":
    print(is_anagram("anagram", "nagaram"))
    print(is_anagram("rat", "car"))
    print(is_anagram("",""))
    print(is_anagram("a", "ab"))

    