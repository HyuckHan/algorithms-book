"""StringHash: Horner's rule 다항식 문자열 해시. hash = hash*B + code(c)를
왼쪽에서 오른쪽으로 누적한다. lecture-notes/lecture07/sections/04_string_hashing.tex의
StringHash pseudocode와 같은 정책(작은 홀수 multiplier)을 따른다."""


# snippet:string-hash:start
def ascii_sum(s):
    return sum(ord(c) for c in s)


def string_hash(s, base=131):
    h = 0
    for c in s:
        h = h * base + ord(c)
    return h
# snippet:string-hash:end

if __name__ == "__main__":
    print("ascii_sum(abcd):", ascii_sum("abcd"))
    print("ascii_sum(dbac):", ascii_sum("dbac"))
    print("string_hash(abcd):", string_hash("abcd"))
    print("string_hash(dbac):", string_hash("dbac"))
    print("string_hash(Apple):", string_hash("Apple"))
    print("string_hash(Apply):", string_hash("Apply"))
