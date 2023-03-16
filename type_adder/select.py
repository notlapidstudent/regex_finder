from __future__ import print_function

import pandas


def get_medical_records_by_type(table: pandas.DataFrame) -> dict:
    """
    Returns ids that are tagged as release or acceptance rows.
    :param table: Table of hospitalizations
    :return: dict of size 2, key for acceptance and another key for release. The values are list of the relevant ids.
    """
    types_for_acceptance = ["תלונת החולה/תלונה עיקרית", "מחלה נוכחית", "רקע רפואי", "רקע", "בדיקה גופנית", "סיכום",
                            "סיכום ותכנית עבודה", "סיכום רופא", "מהלך ודיון"]
    types_for_release = ["מהלך ודיון"]

    return {"קבלה": get_medical_records_by_description_type(table, types_for_acceptance, "min"),
            "שחרור": get_medical_records_by_description_type(table, types_for_release, "max")}


def get_medical_records_by_description_type(table: pandas.DataFrame, text_type: list, action: str) -> list:
    """
    Returns list of row ids which are grouped and selected according to the function parameters
    :param table: Table of hospitalizations
    :param text_type: list of hospitalization types that represent an acceptance or release
    :param action: "min" or "max" the aggregation func that chooses the chosen ids to be returned
    :return: list of ids that are the min or max of their own group.
    """
    ids = []
    table = table.loc[table['Description'].isin(text_type)]

    drop = table[table['DepartmentName'] != table['unit_name']].index
    table = table.drop(drop)
    table['DocumentingTime'] = pandas.to_datetime(table['DocumentingTime'], format='%S:%M.%H')
    table = table.dropna(subset=['DocumentingTime', 'Output_Text'])
    groups = table.groupby(['ID_fake', 'AdmissionNumber_fake', 'Description'])
    for group_id in groups.groups:
        group = groups.get_group(group_id)
        values = group[group['DocumentingTime'] == group['DocumentingTime'].agg(action)]['Medical_Record_TA']
        [ids.append(int(value)) for value in values]

    return ids


def categorise(row: pandas.Series, medical_record_ids_by_type: dict) -> str:
    """
    The function returns the relevant type of the hospitalization for the given row
    :param row: Specific Hospitalization information
    :param medical_record_ids_by_type: Filtered ids of קבלה and שחרור
    :return: אשפוז/קבלה/שחרור
    """
    for type, medical_record_ids in medical_record_ids_by_type.items():
        if row['Medical_Record_TA'] in medical_record_ids:
            return type
    if row['Description'] in ["תלונת החולה / תלונה עקרית"]:
        return "אשפוז"


def add_hospitalization_type(df: pandas.DataFrame):
    """
    Creates a new column according to an existing function
    :param df: Table of hospitalizations
    :param path: File to write the new table
    """

    medical_records_ids_by_type = get_medical_records_by_type(df)
    df['hospitalization_type'] = df.apply(lambda row: categorise(row, medical_records_ids_by_type), axis=1)
    return df
