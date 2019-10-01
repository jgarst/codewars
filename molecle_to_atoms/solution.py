"""Count atoms in a chemical formula."""
from collections import Counter
from enum import Enum
from functools import partial
from itertools import takewhile
from operator import ne
from typing import Dict, Iterator, Optional, Tuple


class Token(Enum):
    """Types of tokens in chemical formulas."""

    NUMBER = 1
    ATOM = 2
    PAREN = 3


PARENS = {
    "(": partial(ne, (Token.PAREN, ")")),
    "{": partial(ne, (Token.PAREN, "}")),
    "[": partial(ne, (Token.PAREN, "]")),
}


def parse_molecule(formula: str) -> Dict[str, int]:
    """
    Given a chemical formula with atoms, fragments and counts,
    return a count of the number of atoms.
    """
    return parse_fragment(tokenize(formula))


def parse_fragment(tokens: Iterator[Tuple[Token, str]]) -> Counter:
    """
    Given an iterator of chemical formula tokens, count the total number of
    atoms present in the formula, until the stop condition is reached.
    """
    atoms: Counter = Counter()
    fragment_count: Optional[Counter] = Counter()

    for token_type, token in tokens:

        if fragment_count is not None:
            multiplicity = int(token) if token_type is Token.NUMBER else 1
            for atom, count in fragment_count.items():
                atoms[atom] += count * multiplicity

            fragment_count = None

        if token_type is Token.PAREN:
            fragment_iter = takewhile(PARENS[token], tokens)
            fragment_count = parse_fragment(fragment_iter)
        elif token_type is Token.ATOM:
            fragment_count = Counter({token: 1})

    if fragment_count is not None:
        atoms += fragment_count

    return atoms


def tokenize(formula: str) -> Iterator[Tuple[Token, str]]:
    """Generate logical elements of a chemical formula."""
    i: int = 0

    while i < len(formula):
        char = formula[i]
        if char.isdigit():
            token_type, (token, i) = Token.NUMBER, tokenize_num(formula, i)
        elif char.isupper():
            token_type, (token, i) = (Token.ATOM, tokenize_atom(formula, i))
        elif char in {"(", "{", "[", "]", "}", ")"}:
            token_type, token, i = Token.PAREN, char, i + 1
        else:
            raise ValueError(
                f"I don't know how to parse {char} at index {i} in {formula}"
            )

        yield token_type, token


def tokenize_num(formula: str, token_start: int) -> Tuple[str, int]:
    """
    Returns a token representing a number, and the termination index of that
    number.
    """
    token_end = token_start + 1
    while token_end < len(formula) and formula[token_end].isdigit():
        token_end += 1

    return formula[token_start:token_end], token_end


def tokenize_atom(formula: str, token_start: int) -> Tuple[str, int]:
    """
    Returns a token representing a chemical element, and the termination
    index of that number.
    """
    if token_start + 1 < len(formula) and formula[token_start + 1].islower():
        return formula[token_start : token_start + 2], token_start + 2

    return (formula[token_start : token_start + 1], token_start + 1)


if __name__ == "__main__":
    print(parse_molecule("H2O"))
    print(parse_molecule("Mg(OH)2"))
    print(parse_molecule("K4[ON(SO3)2]2"))
