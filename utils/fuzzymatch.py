from fuzzywuzzy import fuzz
def fuzzy_match(a: str, b: str) -> int:
    return fuzz.partial_ratio(a, b)