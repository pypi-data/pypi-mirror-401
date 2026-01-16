"""CLI for example package"""

import argparse
from . import hello, add

def main():
    parser = argparse.ArgumentParser(description="Example CLI")
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument("--add", nargs=2, type=int, help="Add two numbers")
    
    args = parser.parse_args()
    
    if args.add:
        result = add(args.add[0], args.add[1])
        print(f"{args.add[0]} + {args.add[1]} = {result}")
    else:
        print(hello(args.name))

if __name__ == "__main__":
    main()