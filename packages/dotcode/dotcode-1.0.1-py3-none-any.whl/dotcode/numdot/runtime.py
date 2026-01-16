def numdot_to_python(code: str) -> str:
    """
    Decode NumDot back into Python source.
    """
    parts = code.strip().split(".")
    try:
        return "".join(chr(int(p)) for p in parts if p.isdigit())
    except Exception:
        raise SyntaxError("Invalid NumDot code")


def run_numdot(code: str):
    source = numdot_to_python(code)
    exec(source, {"__name__": "__main__"})
