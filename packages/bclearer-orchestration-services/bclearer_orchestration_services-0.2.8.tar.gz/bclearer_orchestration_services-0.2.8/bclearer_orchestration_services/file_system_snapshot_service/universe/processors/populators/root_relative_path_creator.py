from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.root_relative_paths import (
    RootRelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.snapshot_domains import (
    SnapshotDomains,
)


# TODO: DZa to ask - should not this be a IndividualFileSystemSnapshotObjects return type?
#  are the compressed files process as a Folder or a different container type?
def create_root_relative_path(
    file_system_object: FileSystemObjects,
    owning_snapshot_domain: SnapshotDomains,
) -> RootRelativePaths:
    root_relative_path = (
        RootRelativePaths()
    )

    if isinstance(
        file_system_object, Folders
    ):
        IndividualFileSystemSnapshotFolders(
            folder=file_system_object,
            owning_snapshot_domain=owning_snapshot_domain,
            relative_path=root_relative_path,
        )

    # TODO: add compressed containers
    else:
        raise TypeError(
            f"Expected Folders instance, but got {type(file_system_object).__name__}. "
            f"Object: {file_system_object}"
        )

    return root_relative_path
