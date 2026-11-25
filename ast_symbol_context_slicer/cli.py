"""CLI for AST Symbol Context Slicer."""
import argparse
from .core import ASTSymbolSlicer


def main():
    parser = argparse.ArgumentParser(description="AST Symbol Context Slicer CLI")
    parser.add_argument("--file", required=True, help="Python file to slice")
    parser.add_argument("--symbol", required=True, help="Target function or class name")
    parser.add_argument("--hops", type=int, default=2, help="Max dependency hops")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        src = f.read()
    slicer = ASTSymbolSlicer(src)
    print(slicer.slice_symbol(args.symbol, max_hops=args.hops))


if __name__ == "__main__":
    main()
