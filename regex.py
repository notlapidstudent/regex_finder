import re


def remove_unessesery_chars_from_title(sentnce: str):
    sentnce = sentnce.replace("=", "")
    sentnce = sentnce.replace(".", "")
    sentnce = sentnce.strip()
    return sentnce


def regex(text: str):
    # pattern = r'(\w+\s+\w+\s+)+(={2,})'
    pattern3 = r'(\.[\w\s]+={2,})'
    matches = re.split(pattern3, text)
    return matches

