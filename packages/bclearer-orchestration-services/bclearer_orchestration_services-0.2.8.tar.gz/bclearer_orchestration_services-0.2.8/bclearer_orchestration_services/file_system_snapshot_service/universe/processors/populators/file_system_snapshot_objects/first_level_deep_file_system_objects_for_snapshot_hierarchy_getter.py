from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)


def get_first_level_children_file_system_object_paths_for_snapshot_hierarchy(
    input_file_system_object: FileSystemObjects,
    extension_to_filter: str,
    parent_file_system_snapshot_folder: IndividualFileSystemSnapshotFolders,
) -> list:
    _ = parent_file_system_snapshot_folder
    # compressed_file = \
    #     check_is_compressed_file(
    #         input_file=input_file_system_object,
    #         report_file_message=True)
    #
    # # TODO: Need to refactor the zipped functionality - STARTED
    # if compressed_file:
    #     zipped_file_children_dictionary = \
    #         get_zipped_file_children_dictionary_for_snapshot_hierarchy(
    #             hierarchy_file_system_object_register=file_system_snapshot_universe_registry,
    #             parent_file_system_snapshot_folder=parent_file_system_snapshot_folder,
    #             child_zipped_folder=input_file_system_object)
    #
    #     zipped_children = \
    #         list(zipped_file_children_dictionary.values())[0]
    #
    #     root_folder_file_system_object_children = \
    #         get_unzipped_children(
    #             temporary_unzipped_files_folder=list(zipped_file_children_dictionary.keys())[0],
    #             parent_file_system_object=input_file_system_object,
    #             zipped_children=zipped_children)
    #
    #     root_folder_children_paths = \
    #         get_paths_from_file_system_objects_at_lower_level(
    #             file_system_object_paths=list(),
    #             file_system_objects=root_folder_file_system_object_children)
    #
    #     return \
    #         root_folder_children_paths
    #
    # else:
    root_path = (
        input_file_system_object.absolute_path
    )

    pattern = (
        f"*{extension_to_filter}"
        if extension_to_filter
        else "*"
    )

    root_folder_children_paths = [
        str(path)
        for path in root_path.glob(
            pattern
        )
    ]

    return root_folder_children_paths
