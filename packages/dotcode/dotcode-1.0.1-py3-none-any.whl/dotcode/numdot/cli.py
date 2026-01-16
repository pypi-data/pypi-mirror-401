import argparse
from .compiler import python_to_numdot
from .runtime import run_numdot, numdot_to_python


def main():
    parser = argparse.ArgumentParser(prog="numdot", description="NumDot esoteric language")
    sub = parser.add_subparsers(dest="cmd")

    c = sub.add_parser("compile")
    c.add_argument("input")
    c.add_argument("-o", "--output")

    r = sub.add_parser("run")
    r.add_argument("input")

    d = sub.add_parser("decode")
    d.add_argument("input")
    d.add_argument("-o", "--output")

    args = parser.parse_args()

    if args.cmd == "compile":
        with open(args.input, "r", encoding="utf-8") as f:
            nd = python_to_numdot(f.read())

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(nd)
        else:
            print(nd)

    elif args.cmd == "run":
        with open(args.input, "r", encoding="utf-8") as f:
            run_numdot(f.read())

    elif args.cmd == "decode":
        with open(args.input, "r", encoding="utf-8") as f:
            py = numdot_to_python(f.read())

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(py)
        else:
            print(py)

    else:
        parser.print_help()
