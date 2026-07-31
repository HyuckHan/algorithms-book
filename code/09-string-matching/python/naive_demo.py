from string_matching import naive_match

if __name__ == "__main__":
    text, pattern = "acebbceeaabceedb", "eeaab"
    matches = naive_match(text, pattern)
    print("matches:", ",".join(str(s) for s in matches))
