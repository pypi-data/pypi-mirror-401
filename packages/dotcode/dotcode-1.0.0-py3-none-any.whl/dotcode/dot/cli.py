import argparse
from .compiler import python_to_dot
from .runtime import run_dot


def main():
    parser = argparse.ArgumentParser(prog="dot", description="Dot esoteric language")
    sub = parser.add_subparsers(dest="cmd")

    c = sub.add_parser("compile")
    c.add_argument("input")
    c.add_argument("-o", "--output")

    r = sub.add_parser("run")
    r.add_argument("input")

    args = parser.parse_args()

    if args.cmd == "compile":
        with open(args.input, "r", encoding="utf-8") as f:
            dot_code = python_to_dot(f.read())

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(dot_code)
        else:
            print(dot_code)

    elif args.cmd == "run":
        with open(args.input, "r", encoding="utf-8") as f:
            run_dot(f.read())

    else:
        parser.print_help()
