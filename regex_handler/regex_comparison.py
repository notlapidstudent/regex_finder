import re

from regex_handler.regexes_store import RegexStore


def find_matching_regexes(paragraph: str) -> dict:
    for regex in RegexStore:
        splitted_paragraph = re.split(regex.value, paragraph)
        if len(splitted_paragraph) > 1:
            return {
                "data": splitted_paragraph,
                "matched_regex": regex.value
            }
        else:
            return {}


