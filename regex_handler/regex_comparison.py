import re
from regexes_store import RegexStore


def find_matching_regexes(paragraph: str) -> dict:
    for regex in RegexStore:
        splitted_paragraph = re.split(regex.value, paragraph)
        if len(splitted_paragraph) > 1:
            return {
                "data": splitted_paragraph,
                "regex_handler": regex.value
            }
        else:
            return {}


