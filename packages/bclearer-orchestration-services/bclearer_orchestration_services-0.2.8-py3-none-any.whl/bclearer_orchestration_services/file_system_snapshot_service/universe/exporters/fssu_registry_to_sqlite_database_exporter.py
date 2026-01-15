from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.sqlite_service.dataframes_dictionary_to_existing_sqlite_as_strings_writer import (
    write_dataframes_dictionary_to_existing_sqlite_as_strings,
)
from bclearer_interop_services.relational_database_services.sqlite_service.sqlite_database_creator import (
    create_sqlite_database,
)


def export_fssu_registry_to_sqlite_database(
    dataframes_dictionary_keyed_on_string: dict,
    test_case_output_folder: Folders,
    fssu_registry_database_base_name: str,
) -> None:
    sqlite_database_file = create_sqlite_database(
        sqlite_database_folder=test_case_output_folder,
        sqlite_database_base_name=fssu_registry_database_base_name,
    )

    write_dataframes_dictionary_to_existing_sqlite_as_strings(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
        sqlite_database_file=sqlite_database_file,
    )
