def python_to_dot(source: str) -> str:
    """
    Encode Python source into Dot language.
    Each character -> '.' repeated ASCII times, space-separated.
    """
    if not source:
        raise ValueError("Empty source code")

    return " ".join("." * ord(ch) for ch in source)
