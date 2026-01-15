from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.import_export.dataframe_to_database_using_engine_exporter import (
    export_dataframe_to_database_using_engine,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.import_export.file_to_temporary_folder_copier import (
    copy_file_to_temporary_folder,
)
from bclearer_interop_services.relational_database_services.sqlalchemy_service.import_export.temporary_file_to_destination_folder_mover import (
    move_temporary_file_to_destination_folder,
)


def export_dataframes_dictionary_to_database_using_engine_via_temporary_folder(
    dataframes_dictionary_keyed_on_string: dict,
    database_file: Files,
    database_engine_creator,
) -> None:
    temporary_database_file = (
        copy_file_to_temporary_folder(
            file=database_file
        )
    )

    database_engine = database_engine_creator(
        database_file=temporary_database_file
    )

    for (
        dataframe_name,
        dataframe,
    ) in (
        dataframes_dictionary_keyed_on_string.items()
    ):
        export_dataframe_to_database_using_engine(
            dataframe_name=dataframe_name,
            dataframe=dataframe,
            database_engine=database_engine,
        )

    database_engine.dispose()

    move_temporary_file_to_destination_folder(
        temporary_file=temporary_database_file,
        destination_folder=database_file.parent_folder,
    )
