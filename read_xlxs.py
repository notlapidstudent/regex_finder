import re
import pandas as pd
from pandas import DataFrame

from regex import remove_unessesery_chars_from_title


def read_csv(path: str):
    with open(path) as f:
        df = pd.read_csv(f)
    return df


def write_csv(df: DataFrame):
    df.to_csv("test.csv", index=False, encoding='utf-8-sig')


def add_colums(df: DataFrame):
    df["sub_type"] = ''
    df["sub_type_info"] = ''
    return df


def regex(text: str):
    pattern3 = r'(\.[\w\s]+={2,})'
    matches = re.split(pattern3, text)
    return matches


def add_row_by_equals_regex(df: DataFrame):
    for j, row in df.iterrows():
        if type(row["Output_Text"]) == str and row["Output_Text"]:
            row['Output_Text'] = row['Output_Text']
            matches = regex(row['Output_Text'])
            if len(matches) > 1:
                i = 1
                while i < len(matches) - 1:
                    matches[i] = remove_unessesery_chars_from_title(matches[i])
                    df2 = pd.DataFrame([{"DepartmentName": row["DepartmentName"],
                                         "Medical_Record_TA": row["Medical_Record_TA"],
                                         "Description": row["Description"],
                                         "DocumentingTime": row["DocumentingTime"],
                                         "unit_name": row["unit_name"],
                                         "Output_Text": row["Output_Text"],
                                         "ID_fake": row["ID_fake"],
                                         "AdmissionNumber_fake": row["AdmissionNumber_fake"],
                                         "sub_type": matches[i],
                                         "sub_type_info": matches[i + 1]}])
                    df.drop(j, inplace=True)
                    df = pd.concat([df, df2])
                    i = i + 2

    return df


def activate(df: DataFrame):
    df = add_colums(df)
    df = add_row_by_equals_regex(df)
    df = df.drop(["Index"], axis=1)
    df.sort_values(by=['Medical_Record_TA'], ascending=True, inplace=True)
    return df
