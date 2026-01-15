import msaccessdb
from bclearer_core.configurations.b_import_export_configurations.b_export_database_configurations import (
    BExportDatabaseConfigurations,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.access_service.access.dataframes_dictionary_to_existing_access_as_strings_writer import (
    write_dataframes_dictionary_to_existing_access_as_strings,
)


def write_dataframes_dictionary_to_new_access_as_strings(
    dataframes_dictionary_keyed_on_string: dict,
    access_database_file: Files,
) -> None:
    # TODO add checks - assume that the file DOES already exist
    if access_database_file.exists():
        # TODO add checks - log etc.
        return

    msaccessdb.create(
        filespec=access_database_file.absolute_path_string
    )

    BExportDatabaseConfigurations.EXPORT_AS_SHORT_TEXT = (
        True
    )

    write_dataframes_dictionary_to_existing_access_as_strings(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
        access_database_file=access_database_file,
    )
