# Group Anagrams
# Input: ["eat","tea","tan","ate","nat","bat"]
# Output: [["eat","tea","ate"],["tan","nat"],["bat"]]

def group_anagrams(strs):
    groups = {}

    for word in strs:
        key = "".join(sorted(word)) #sort to create key

        if key not in groups:
            groups[key] = []
        groups[key].append(word)

    return list(groups.values())


if __name__ ==  "__main__" :
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(group_anagrams(words))

# Time Complexity:
# O(n * klogk)
# n = number of words
# k = max length of word

# Space Complexity:
# O(n * k) for dictonry