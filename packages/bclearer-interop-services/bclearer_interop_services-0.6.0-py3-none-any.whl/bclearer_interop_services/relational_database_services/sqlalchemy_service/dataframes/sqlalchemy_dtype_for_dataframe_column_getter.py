from pandas import Series
from sqlalchemy import String, Text


def get_sqlalchemy_dtype_for_dataframe_column(
    column_series: Series,
):
    max_short_text = 255

    max_len = (
        column_series.dropna()
        .astype(str)
        .str.len()
        .max()
    )

    if (
        max_len
        and max_len > max_short_text
    ):
        return Text

    else:
        return String(max_short_text)
