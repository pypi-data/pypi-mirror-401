from pathlib import Path

from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.non_root_relative_paths import (
    NonRootRelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.relative_paths import (
    RelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_files import (
    IndividualFileSystemSnapshotFiles,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_objects import (
    IndividualFileSystemSnapshotObjects,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.snapshot_domains import (
    SnapshotDomains,
)


def create_child_file_system_snapshot_object(
    parent_file_system_snapshot_folder: IndividualFileSystemSnapshotFolders,
    child_path_string: str,
    owning_snapshot_domain: SnapshotDomains,
) -> (
    IndividualFileSystemSnapshotObjects
):
    child_path = Path(child_path_string)

    parent_relative_path_bie_object = parent_file_system_snapshot_folder.extended_objects[
        BieFileSystemSnapshotDomainTypes.BIE_RELATIVE_PATHS
    ]

    if not isinstance(
        parent_relative_path_bie_object,
        RelativePaths,
    ):
        raise TypeError

    parent_relative_path = (
        parent_relative_path_bie_object.relative_path
    )

    relative_path_child = (
        parent_relative_path
        / child_path.name
    )

    relative_path_bie_object = NonRootRelativePaths(
        relative_path=relative_path_child,
        relative_path_parent=parent_relative_path_bie_object,
    )

    if child_path.is_dir():
        child_file_system_snapshot_object = IndividualFileSystemSnapshotFolders(
            folder=Folders(
                absolute_path=child_path
            ),
            owning_snapshot_domain=owning_snapshot_domain,
            relative_path=relative_path_bie_object,
        )

    elif child_path.is_file():
        child_file_system_snapshot_object = IndividualFileSystemSnapshotFiles(
            file=Files(
                absolute_path=child_path
            ),
            owning_snapshot_domain=owning_snapshot_domain,
            relative_path=relative_path_bie_object,
        )

    else:
        raise NotImplementedError

    return child_file_system_snapshot_object
