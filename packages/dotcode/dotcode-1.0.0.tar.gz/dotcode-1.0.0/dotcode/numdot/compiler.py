def python_to_numdot(source: str) -> str:
    """
    Encode Python source into NumDot language.
    Each character -> <ASCII>.
    """
    if not source:
        raise ValueError("Empty source code")

    return "".join(f"{ord(ch)}." for ch in source)
