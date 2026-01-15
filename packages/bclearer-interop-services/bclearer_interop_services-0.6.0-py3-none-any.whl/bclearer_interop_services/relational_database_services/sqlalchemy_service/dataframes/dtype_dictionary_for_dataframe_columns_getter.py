from bclearer_interop_services.relational_database_services.sqlalchemy_service.dataframes.sqlalchemy_dtype_for_dataframe_column_getter import (
    get_sqlalchemy_dtype_for_dataframe_column,
)
from pandas import DataFrame


def get_dtype_dictionary_for_dataframe_columns(
    dataframe: DataFrame,
) -> dict:
    dtype_dictionary = dict()

    for (
        column_name
    ) in dataframe.columns:
        column_dtype = get_sqlalchemy_dtype_for_dataframe_column(
            column_series=dataframe[
                column_name
            ]
        )

        if column_dtype is not None:
            dtype_dictionary[
                column_name
            ] = column_dtype

    return dtype_dictionary
