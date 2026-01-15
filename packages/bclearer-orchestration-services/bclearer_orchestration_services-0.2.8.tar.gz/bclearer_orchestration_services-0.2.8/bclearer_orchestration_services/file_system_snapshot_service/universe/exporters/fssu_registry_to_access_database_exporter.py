from pathlib import Path

from bclearer_interop_services.file_system_service.file_system_paths.constants.file_system_file_extensions import (
    FileSystemFileExtensions,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.relational_database_services.access_service.access.dataframes_dictionary_to_new_access_as_strings_writer import (
    write_dataframes_dictionary_to_new_access_as_strings,
)


def export_fssu_registry_to_access_database(
    dataframes_dictionary_keyed_on_string: dict,
    test_case_output_folder: Folders,
    fssu_registry_database_base_name: str,
) -> None:
    access_database_file_name = (
        fssu_registry_database_base_name
        + FileSystemFileExtensions.ACCDB.delimited_file_extension
    )

    access_database_file = test_case_output_folder.get_descendant_file_system_file(
        relative_path=Path(
            access_database_file_name
        )
    )

    write_dataframes_dictionary_to_new_access_as_strings(
        dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
        access_database_file=access_database_file,
    )
