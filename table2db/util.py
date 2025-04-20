def normalize_delimiter(s: str) -> str:
    if s == "\\t":
        return "\t"
    return s or ","

