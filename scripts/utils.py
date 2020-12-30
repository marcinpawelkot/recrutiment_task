import urllib.request
from typing import Any, Optional, List, Dict

import ndjson
import pandas as pd

import config


def load_input_data(file_name: str) -> List[Dict]:
    with urllib.request.urlopen(config.DATA_SOURCES[file_name]) as url:
        data = ndjson.loads(url.read().decode())
    return data


def flatten_json(nested_json: Dict) -> Dict:
    out = {}

    def flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


def parse_to_df(dicts: List[Dict], table_name: str) -> pd.DataFrame:
    if table_name == "observation":
        df = pd.DataFrame(
            [
                flatten_json(
                    {
                        k: v
                        for k, v in dict_data.items()
                        if k in config.COLUMNS_NAMES[table_name]
                    }
                )
                for dict_data in dicts
            ]
        )
        df["component"] = pd.DataFrame(dicts)["component"]
        df = df.explode("component").reset_index(drop=True)
        parsed_component = _parse_component(df)
        df.drop(parsed_component.index, inplace=True)
        result = pd.concat([parsed_component, df])
        _add_db_id(result)
        return result
    else:
        df = pd.DataFrame(
            [
                flatten_json(
                    {
                        k: v
                        for k, v in dict_data.items()
                        if k in config.COLUMNS_NAMES[table_name]
                    }
                )
                for dict_data in dicts
            ]
        )
        _add_db_id(df)
        return df


def _parse_component(df: pd.DataFrame) -> pd.DataFrame:
    component_array = df["component"][~df["component"].isnull()]
    parsed = pd.DataFrame(
        [flatten_json(row) for row in component_array], index=component_array.index
    )
    return parsed


def _add_db_id(df: pd.DataFrame) -> None:
    df.index = df.index + 1
    df["db_id"] = df.index.astype(int)


def insert_relation_column(
        parent_df: pd.DataFrame,
        child_df: pd.DataFrame,
        parent_df_name: str,
        reference_col: str,
) -> None:
    child_df[parent_df_name + "_id"] = (
        child_df[reference_col].str.split(pat="/", expand=True)[1].astype(str)
    )
    idx = pd.Series(
        pd.merge(
            child_df[parent_df_name + "_id"],
            parent_df[["db_id", "id"]],
            how="left",
            left_on=parent_df_name + "_id",
            right_on="id",
        )["db_id"],
        dtype="Int64",
    )
    idx.index = idx.index + 1
    child_df[parent_df_name + "_db_id"] = idx


def format_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series.astype(str).str[:10]).dt.date


def remove_null_required_fields(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    df.dropna(subset=config.REQUIRED_COLUMNS_NAMES[table_name], inplace=True)


def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r"\N"
    return str(value).replace("\n", "\\n")
