import pandas as pd
from pandas import DataFrame

from utils import remove_unessesery_chars_from_title
from regex_handler.regex_comparison import find_matching_regexes


def add_colums(df: DataFrame) -> DataFrame:
    df["sub_type"] = ''
    df["sub_type_info"] = ''
    df["regex_handler"] = ''
    return df


def add_row_by_equals_regex(df: DataFrame) -> DataFrame:
    for j, row in df.iterrows():
        if type(row["Output_Text"]) == str and row["Output_Text"]:
            matches = find_matching_regexes(row['Output_Text'])
            if matches:
                i = 1
                df.drop(j, inplace=True)
                data = matches.get('data')
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
                                         "regex_handler": matches.get("regex_handler")
                                         }])
                    df = pd.concat([df, df2])
                    i = i + 2
    return df


def enrich_data(df: DataFrame, **kwargs) -> DataFrame:
    if "fuzzy_percentage" in kwargs:
        df["percentage"] = ''
    df = add_colums(df)
    df = add_row_by_equals_regex(df)
    df = df.drop(["Index"], axis=1)
    df.sort_values(by=['Medical_Record_TA'], ascending=True, inplace=True)
    return df
