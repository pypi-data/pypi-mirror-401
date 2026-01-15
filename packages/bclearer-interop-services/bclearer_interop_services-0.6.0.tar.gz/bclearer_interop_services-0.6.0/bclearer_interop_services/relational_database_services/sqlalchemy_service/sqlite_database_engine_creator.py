from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from sqlalchemy import (
    Engine,
    create_engine,
)


def create_sqlite_database_engine(
    database_file: Files,
) -> Engine:
    db_path = (
        database_file.absolute_path_string
    )

    # TODO: remove strings
    sqlite_database_engine_url = (
        f"sqlite:///{db_path}"
    )

    sqlite_database_engine = (
        create_engine(
            sqlite_database_engine_url
        )
    )

    return sqlite_database_engine
