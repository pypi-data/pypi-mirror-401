from typing import List

from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_objects import (
    IndividualFileSystemSnapshotObjects,
)


def filter_individual_file_system_snapshot_objects_by_extension_list(
    individual_file_system_snapshot_objects: List[
        IndividualFileSystemSnapshotObjects
    ],
    extensions: list,
) -> list:
    individual_file_system_snapshot_objects_filtered = (
        list()
    )

    for individual_file_system_snapshot_object in individual_file_system_snapshot_objects:
        if (
            individual_file_system_snapshot_object.file_system_object_properties.extension
            in extensions
        ):
            individual_file_system_snapshot_objects_filtered.append(
                individual_file_system_snapshot_object
            )

    return individual_file_system_snapshot_objects_filtered
