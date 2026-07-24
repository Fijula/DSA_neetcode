# Valid Anagram
# Given two strings s and t, return True if t is an anagram of s.
# Example: s="anagram", t="nagaram" -> True
#          s="rat",     t="car"     -> False


# Case 1: Brute force: sort both strings and compare
def is_anagram_brute(s, t):
    if len(s) != len(t):          
        return False
    return sorted(s) == sorted(t)  
# Time:  O(n log n)   
# Space: O(n)         


# Case 2: Optimal: count characters with a hash map
def is_anagram_optimal(s, t):
    if len(s) != len(t):
        return False
    counts = {}                    
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1   
    for ch in t:
        if ch not in counts or counts[ch] == 0:
            return False           
        counts[ch] -= 1
    return True
# Time:  O(n)
# Space: O(n)  


# Case 3: Counter concepts single line
def is_anagram_short(s, t):
    from collections import Counter
    return Counter(s) == Counter(t)   # Counter builds a char->count map, compares
# Time: O(n), Space: O(n)


if __name__ == "__main__":
    print(is_anagram_brute("anagram", "nagaram"))   # True
    print(is_anagram_optimal("rat", "car"))         # False
    print(is_anagram_short("listen", "silent"))     # True
