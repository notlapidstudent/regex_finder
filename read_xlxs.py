import re
import pandas as pd
from pandas import DataFrame

from regex import remove_unessesery_chars_from_title


def read_csv(path: str):
    with open(path) as f:
        df = pd.read_csv(f)
    return df


def write_csv(df: DataFrame):
    df.to_csv("test1.csv", index=False, encoding='utf-8-sig')


def add_colums(df: DataFrame):
    df["sub_type"] = ''
    df["sub_type_info"] = ''
    df["regex"] = ''
    df["percentage"] = ''
    return df


def regex(text: str) -> dict:
    pattern3 = r'(\.[\w\s]+={2,})'
    matches = re.split(pattern3, text)
    return matches


def add_row_by_equals_regex(df: DataFrame):
    for j, row in df.iterrows():
        if type(row["Output_Text"]) == str and row["Output_Text"]:
            matches = regex(row['Output_Text'])
            if matches:
                i = 1
                df.drop(j, inplace=True)
                data=matches.get('data')
                while i < len(data) - 1:
                    data[i] = remove_unessesery_chars_from_title(data[i])
                    df2 = pd.DataFrame([{"DepartmentName": row["DepartmentName"],
                                         "Medical_Record_TA": row["Medical_Record_TA"],
                                         "Description": row["Description"],
                                         "DocumentingTime": row["DocumentingTime"],
                                         "unit_name": row["unit_name"],
                                         "Output_Text": row["Output_Text"],
                                         "ID_fake": row["ID_fake"],
                                         "AdmissionNumber_fake": row["AdmissionNumber_fake"],
                                         "sub_type": data[i],
                                         "sub_type_info": data[i + 1],
                                         "regex": matches.get("regex")
                                         }])
                    df = pd.concat([df, df2])
                    i = i + 2
    return df


def activate(df: DataFrame):
    df = add_colums(df)
    df = add_row_by_equals_regex(df)
    df = df.drop(["Index"], axis=1)
    df.sort_values(by=['Medical_Record_TA'], ascending=True, inplace=True)
    return df
