#!/usr/bin/env python3
"""
passgen.py - Secure password generator (uses the `secrets` module).

Examples:
    python passgen.py -l 16 -ULS        # 16 chars: Upper + Lower + Symbols
    python passgen.py -l 20 -ULSN       # add Numbers
    python passgen.py -l 12 -UL -c 5    # five 12-char passwords
    python passgen.py                   # interactive mode (prompts for everything)
"""

import argparse
import secrets
import string
import sys

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/~"
AMBIGUOUS = "O0oIl1|`'\""
MIN_LENGTH = 4
MAX_LENGTH = 256


def build_pools(upper, lower, symbols, numbers, no_ambiguous):
    pools = []
    if upper:
        pools.append(string.ascii_uppercase)
    if lower:
        pools.append(string.ascii_lowercase)
    if numbers:
        pools.append(string.digits)
    if symbols:
        pools.append(SYMBOLS)
    if no_ambiguous:
        pools = ["".join(c for c in p if c not in AMBIGUOUS) for p in pools]
    return pools


def generate(length, pools):
    """Generate one password containing at least one char from every pool."""
    if length < len(pools):
        raise ValueError(f"Length must be at least {len(pools)} for the selected options.")

    all_chars = "".join(pools)
    # Guarantee one character from each selected set...
    chars = [secrets.choice(p) for p in pools]
    # ...then fill the rest from the combined pool.
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    # Cryptographically secure shuffle so guaranteed chars aren't predictable in position.
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def prompt_length():
    while True:
        raw = input(f"Password length ({MIN_LENGTH}-{MAX_LENGTH}): ").strip()
        if raw.isdigit() and MIN_LENGTH <= int(raw) <= MAX_LENGTH:
            return int(raw)
        print(f"  Please enter a number between {MIN_LENGTH} and {MAX_LENGTH}.")


def prompt_options():
    print("Character sets (y/n):")
    answers = {}
    for key, label in [("U", "Uppercase"), ("L", "Lowercase"),
                       ("N", "Numbers"), ("S", "Symbols")]:
        answers[key] = input(f"  Include {label}? [Y/n]: ").strip().lower() != "n"
    return answers["U"], answers["L"], answers["S"], answers["N"]


def parse_args():
    p = argparse.ArgumentParser(
        description="Generate secure random passwords.",
        epilog="Example: passgen.py -l 16 -ULS",
    )
    p.add_argument("-l", "--length", type=int, help="password length")
    p.add_argument("-U", "--upper", action="store_true", help="include Uppercase letters")
    p.add_argument("-L", "--lower", action="store_true", help="include Lowercase letters")
    p.add_argument("-S", "--symbols", action="store_true", help="include Symbols")
    p.add_argument("-N", "--numbers", action="store_true", help="include Numbers")
    p.add_argument("-c", "--count", type=int, default=1, help="how many passwords (default 1)")
    p.add_argument("-x", "--no-ambiguous", action="store_true",
                   help="exclude look-alike characters (O/0, l/1/I, quotes, etc.)")
    return p.parse_args()


def main():
    args = parse_args()

    # Length: ask if not supplied
    length = args.length if args.length is not None else prompt_length()
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        sys.exit(f"Error: length must be between {MIN_LENGTH} and {MAX_LENGTH}.")

    # Character sets: ask if no flags supplied
    if any([args.upper, args.lower, args.symbols, args.numbers]):
        upper, lower, symbols, numbers = args.upper, args.lower, args.symbols, args.numbers
    else:
        upper, lower, symbols, numbers = prompt_options()

    pools = build_pools(upper, lower, symbols, numbers, args.no_ambiguous)
    if not pools:
        sys.exit("Error: select at least one character set (-U, -L, -S, -N).")

    try:
        for _ in range(max(1, args.count)):
            print(generate(length, pools))
    except ValueError as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
