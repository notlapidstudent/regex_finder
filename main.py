import pandas as pd
from pandas import DataFrame

from data_handle import enrich_data


def read_csv(path: str):
    with open(path) as f:
        df = pd.read_csv(f)
    return df


def write_csv(df: DataFrame):
    df.to_csv("test1.csv", index=False, encoding='utf-8-sig')



if __name__ == '__main__':
    write_csv(enrich_data(read_csv('C:\\Users\\student28\\Desktop\\files\\output-mutmam.csv')))
