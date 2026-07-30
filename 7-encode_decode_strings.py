# Encode and Decode Strings
# Design encode(list_of_strings) -> string and decode(string) -> list_of_strings
# so that decode(encode(strs)) == strs. The encoded string is sent over a network.
# The strings can contain ANY characters, including digits, "#" and "".
# Example: ["Hello","World"] -> "5#Hello5#World" -> ["Hello","World"]
#          [""]              -> "0#"             -> [""]


# Case 1: Naive: join with a separator character  (BROKEN - here to show why)
def encode_naive(strs):
    return "#".join(strs)                 # looks fine...

def decode_naive(s):
    return s.split("#")                   # ...until a string itself contains "#"
# Fails on ["a#b", "c"] -> "a#b#c" -> ["a", "b", "c"]   wrong, 3 strings not 2
# There is no character that is guaranteed safe, so no separator alone can work.


# Case 2: Optimal: length prefix - "<len>#<string>" for each string
def encode(strs):
    result = ""
    for s in strs:
        result += str(len(s)) + "#" + s   # the "#" only ends the NUMBER, never the text
    return result
9252204535
def decode(s):
    result = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != "#":                # walk forward to the delimiter
            j += 1
        length = int(s[i:j])              # digits before "#" are the length
        start = j + 1                     # text begins right after "#"
        result.append(s[start:start + length])
        i = start + length                # jump past the text to the next block
    return result
# Time:  O(n)   n = total characters across all strings
# Space: O(n)   for the encoded string / decoded list
#


# Case 3: Short: same idea, built with a comprehension
def encode_short(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode_short(s):
    result, i = [], 0
    while i < len(s):
        j = s.index("#", i)               # index() finds the delimiter for us
        length = int(s[i:j])
        result.append(s[j + 1:j + 1 + length])
        i = j + 1 + length
    return result
# Time: O(n), Space: O(n)


if __name__ == "__main__":
    cases = [
        ["Hello", "World"],
        [""],
        ["neet", "code", "love", "you"],
        ["a#b", "c"],                     # contains the delimiter
        ["4#tricky", "", "12"],           # digits and "#" inside the text
    ]

    for strs in cases:
        print(strs, "->", encode(strs), "->", decode(encode(strs)),
              decode(encode(strs)) == strs)

    print(decode_short(encode_short(["a#b", "c"])))   # ['a#b', 'c']
    print(decode_naive(encode_naive(["a#b", "c"])))   # ['a', 'b', 'c']  <- broken
