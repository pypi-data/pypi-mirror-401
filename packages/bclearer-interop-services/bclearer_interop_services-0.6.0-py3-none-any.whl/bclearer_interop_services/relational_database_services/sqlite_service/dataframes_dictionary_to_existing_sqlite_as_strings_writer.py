from bclearer_core.configurations.b_import_export_configurations.b_export_database_configurations import (
    BExportDatabaseConfigurations,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.import_export.dataframes_dictionary_to_database_using_engine_via_temporary_folder_exporter import (
    export_dataframes_dictionary_to_database_using_engine_via_temporary_folder,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.sqlite_database_engine_creator import (
    create_sqlite_database_engine,
)


def write_dataframes_dictionary_to_existing_sqlite_as_strings(
    dataframes_dictionary_keyed_on_string: dict,
    sqlite_database_file: Files,
) -> None:
    # TODO add checks - assume that the file DOES already exist
    if (
        not sqlite_database_file.exists()
    ):
        # TODO add checks - log etc.
        # TODO remove create
        pass

    BExportDatabaseConfigurations.EXPORT_AS_SHORT_TEXT = (
        True
    )

    export_dataframes_dictionary_to_database_using_engine_via_temporary_folder(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
        database_file=sqlite_database_file,
        database_engine_creator=create_sqlite_database_engine,
    )
