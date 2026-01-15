import urllib

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from sqlalchemy import (
    Engine,
    create_engine,
)


def create_access_database_engine(
    database_file: Files,
) -> Engine:
    # TODO: remove strings
    odbc_string = (
        "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        + f"DBQ={database_file.absolute_path_string};"
    )

    odbc_string_encoded = (
        urllib.parse.quote_plus(
            odbc_string
        )
    )

    # TODO: remove strings
    access_database_engine_url = f"access+pyodbc:///?odbc_connect={odbc_string_encoded}"

    access_database_engine = (
        create_engine(
            access_database_engine_url
        )
    )

    return access_database_engine
