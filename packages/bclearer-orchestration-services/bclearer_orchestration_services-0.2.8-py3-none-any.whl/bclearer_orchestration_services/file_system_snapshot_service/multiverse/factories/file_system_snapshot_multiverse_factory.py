from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_configurations import (
    FolderConfigurations,
)


# TODO: create length variable and check via case match - extract out as a factory within a factories folder
def create_file_system_snapshot_multiverse(
    input_snapshot_containers_folder_configuration: FolderConfigurations,
):
    # TODO: would it be a good idea to store this number and pass it to the Multiverse initialisation and store it as
    #  its "multiverse input cardinality" for future checks?
    input_root_file_system_objects_count = len(
        input_snapshot_containers_folder_configuration.folder_list
    )

    # TODO: find a better exception - or maybe even don't check this at this level, but at the caller's level?
    if (
        input_root_file_system_objects_count
        < 1
    ):
        raise FileExistsError

    file_system_snapshot_multiverse = (
        FileSystemSnapshotMultiverses()
    )

    return (
        file_system_snapshot_multiverse
    )
