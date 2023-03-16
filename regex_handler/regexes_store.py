from enum import Enum


class RegexStore(Enum):
    ULTIMATE_REGEX='(\n[\w\s]+[\w]?[\s]*[:]?[\s]*\n={3,}|\n[\w\s]+[\w]?[\s]*[:]?[\s]*\n-{3,}|\n[-]?[\w\s]+[\w]?[\s]*[:]?[\s]*\n)'
    # S = "(\.[\w\s]+={2,})"
    # MINUSES = "(\n[\w\s]+[\w]?[\s]*:?[\s]*\n-{3,})"
    # EQUALISES = "(\n[\w\s]+\n={3,})"

