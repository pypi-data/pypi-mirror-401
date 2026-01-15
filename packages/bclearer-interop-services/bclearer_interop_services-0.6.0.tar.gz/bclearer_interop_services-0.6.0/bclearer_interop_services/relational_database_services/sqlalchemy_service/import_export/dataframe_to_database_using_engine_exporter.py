from bclearer_core.configurations.b_import_export_configurations.b_export_database_configurations import (
    BExportDatabaseConfigurations,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.dataframes.dtype_dictionary_for_dataframe_columns_getter import (
    get_dtype_dictionary_for_dataframe_columns,
)
from pandas import DataFrame
from sqlalchemy import Engine


def export_dataframe_to_database_using_engine(
    dataframe_name: str,
    dataframe: DataFrame,
    database_engine: Engine,
) -> None:
    if (
        BExportDatabaseConfigurations.EXPORT_AS_SHORT_TEXT
    ):
        dtype = get_dtype_dictionary_for_dataframe_columns(
            dataframe=dataframe
        )

    else:
        dtype = None

    dataframe.to_sql(
        name=dataframe_name,
        con=database_engine,
        if_exists="replace",  # "replace", "append", or "fail"
        index=False,  # whether to write the DataFrame index
        dtype=dtype,
    )
