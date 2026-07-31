from string_matching import build_lps, kmp_search

if __name__ == "__main__":
    lps = build_lps("BAABABAA")
    print("lps:", ",".join(str(v) for v in lps))
    text, pattern = "acebbceeaabceedb", "eeaab"
    matches = kmp_search(text, pattern)
    print("matches:", ",".join(str(s) for s in matches))
