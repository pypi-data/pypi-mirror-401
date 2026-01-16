def dot_to_python(code: str) -> str:
    """
    Decode Dot language back into Python source.
    """
    groups = code.strip().split()
    try:
        return "".join(chr(len(group)) for group in groups if group)
    except Exception:
        raise SyntaxError("Invalid Dot code")


def run_dot(code: str):
    source = dot_to_python(code)
    exec(source, {"__name__": "__main__"})
