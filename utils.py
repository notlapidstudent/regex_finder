import re


def remove_unessesery_chars_from_title(sentence: str) -> str:
    sentence = sentence.replace("=", "")
    sentence = sentence.replace(".", "")
    sentence = re.sub(r"[^\u0590-\u05FF\s]+", "", sentence)
    sentence = sentence.strip()
    return sentence
