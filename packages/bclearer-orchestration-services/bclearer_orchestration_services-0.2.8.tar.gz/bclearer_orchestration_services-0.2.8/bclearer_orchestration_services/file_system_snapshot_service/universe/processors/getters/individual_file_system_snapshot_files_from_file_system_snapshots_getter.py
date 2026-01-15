from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_files import (
    IndividualFileSystemSnapshotFiles,
)


# TODO: promote to nf_common? - DONE - type the list
def get_individual_file_system_snapshot_files_from_file_system_snapshots(
    file_system_snapshots: list,
) -> list:
    individual_file_system_snapshot_files = [
        individual_file_system_snapshot_file
        for individual_file_system_snapshot_file in file_system_snapshots
        if isinstance(
            individual_file_system_snapshot_file,
            IndividualFileSystemSnapshotFiles,
        )
    ]

    return individual_file_system_snapshot_files
