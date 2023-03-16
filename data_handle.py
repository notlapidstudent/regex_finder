import pandas as pd
from pandas import DataFrame

from fuzzy_typos.fuzzy_fix import fix_typos_on_subtype_description
from regex_handler.regex_comparison import find_matching_regexes
from type_adder.select import add_hospitalization_type
from utils import remove_unessesery_chars_from_title


def add_index_day(df: DataFrame) -> DataFrame:
    df["date"] = pd.to_datetime(df["DocumentingTime"], format='%S:%M.%H').dt.date
    df["index_day"] = df.groupby(["ID_fake", "AdmissionNumber_fake", "date"]).ngroup() + 1
    return df


def add_row_by_equals_regex(df: DataFrame, **kwargs) -> DataFrame:
    df["sub_type"] = ''
    df["sub_type_info"] = ''

    for j, row in df.iterrows():
        if type(row["Output_Text"]) == str and row["Output_Text"]:
            matches = find_matching_regexes(row['Output_Text'])
            if matches:
                i = 1
                df.drop(j, inplace=True)
                data = matches.get('data')
                while i < len(data) - 1:
                    data[i] = remove_unessesery_chars_from_title(data[i])
                    if "matched_regex" in kwargs:
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
                                             "matched_regex": matches.get("matched_regex")
                                             }])
                    else:
                        df2 = pd.DataFrame([{"DepartmentName": row["DepartmentName"],
                                             "Medical_Record_TA": row["Medical_Record_TA"],
                                             "Description": row["Description"],
                                             "DocumentingTime": row["DocumentingTime"],
                                             "unit_name": row["unit_name"],
                                             "Output_Text": row["Output_Text"],
                                             "ID_fake": row["ID_fake"],
                                             "AdmissionNumber_fake": row["AdmissionNumber_fake"],
                                             "sub_type": data[i],
                                             "sub_type_info": data[i + 1]
                                             }])

                    df = pd.concat([df, df2])
                    i = i + 2
    return df


def enrich_data(df: DataFrame, hospitalization_type=True, **kwargs) -> DataFrame:
    if "matched_regex" in kwargs:
        df["matched_regex"] = ''
        df = add_row_by_equals_regex(df, matched_regex=True)
    else:
        df = add_row_by_equals_regex(df)

    if "fuzzy_percentage" in kwargs:
        df = fix_typos_on_subtype_description(df)

    if hospitalization_type:
        df = add_hospitalization_type(df)

    df = add_index_day(df)
    df = df.drop(["Index", "date"], axis=1)
    df.sort_values(by=['Medical_Record_TA'], ascending=True, inplace=True)
    return df
