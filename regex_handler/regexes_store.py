from enum import Enum


class RegexStore(Enum):
    # S = "(\.[\w\s]+={2,})"
    MINUSES = "(\n[\w\s]+[\w]?[\s]*:?[\s]*\n-{3,})"
    EQUALISES = "(\n[\w\s]+\n={3,})"
    O = ""
    A = ""
    P = ""
