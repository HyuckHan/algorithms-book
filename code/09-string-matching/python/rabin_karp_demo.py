from string_matching import rabin_karp

if __name__ == "__main__":
    text, pattern = "acebbceeaabceedb", "eeaab"
    matches = rabin_karp(text, pattern, 5, 113)
    print("matches:", ",".join(str(s) for s in matches))
