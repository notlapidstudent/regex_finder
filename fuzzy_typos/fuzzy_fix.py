from fuzzywuzzy import fuzz
from pandas import DataFrame
from fuzzy_typos.fuzzy_words import FuzzyWords


# def fix_typos_on_subtype_description(df: DataFrame) -> DataFrame:
#     for j, row in df.iterrows():
#         if row['sub_type']:
#             values = _replace_similarities(row)
#             df.at[j, 'sub_type'] = values[0]
#             df.at[j, 'fuzz_percentage'] = values[1]
#     return df


# def _replace_similarities(row):
#     for word in FuzzyWords:
#         ratio = fuzz.ratio(row['sub_type'], word.value)
#         if ratio > 60:
#             return (word.value, ratio)
#
#     return row['sub_type'], 0


def fix_typos_on_subtype_description(df: DataFrame) -> DataFrame:
    df['sub_type'] = df['sub_type'].apply(_replace_similarities)
    return df


def _replace_similarities(sentence):
    for word in FuzzyWords:
        if fuzz.ratio(sentence, word.value) > 85:
            return word.value
    return sentence
