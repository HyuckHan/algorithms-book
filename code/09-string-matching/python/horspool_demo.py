from string_matching import build_horspool_shift, horspool_search

if __name__ == "__main__":
    tiger_shift, _ = build_horspool_shift("TIGER")
    rational_shift, _ = build_horspool_shift("RATIONAL")
    print("shift_I:", tiger_shift["I"])
    print("shift_A:", rational_shift["A"])
    text, pattern = "acebbceeaabceedb", "eeaab"
    matches = horspool_search(text, pattern)
    print("matches:", ",".join(str(s) for s in matches))
