from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_objects import (
    IndividualFileSystemSnapshotObjects,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def populate_universe_individual_file_system_snapshot_objects(
    file_system_snapshot_universe_registry,
    universe_individual_file_system_snapshot_objects: list,
) -> None:
    from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
        FileSystemSnapshotUniverseRegistries,
    )

    if not isinstance(
        file_system_snapshot_universe_registry,
        FileSystemSnapshotUniverseRegistries,
    ):
        raise TypeError

    __add_individual_file_system_snapshot_object_to_list(
        universe_individual_file_system_snapshot_objects=universe_individual_file_system_snapshot_objects,
        individual_file_system_snapshot_object=file_system_snapshot_universe_registry.root_relative_path.snapshot,
    )


def __add_individual_file_system_snapshot_object_to_list(
    universe_individual_file_system_snapshot_objects: list,
    individual_file_system_snapshot_object: IndividualFileSystemSnapshotObjects,
) -> None:
    universe_individual_file_system_snapshot_objects.append(
        individual_file_system_snapshot_object
    )

    if isinstance(
        individual_file_system_snapshot_object,
        IndividualFileSystemSnapshotFolders,
    ):
        for (
            snapshot_part
        ) in (
            individual_file_system_snapshot_object.parts
        ):
            __add_individual_file_system_snapshot_object_to_list(
                universe_individual_file_system_snapshot_objects=universe_individual_file_system_snapshot_objects,
                individual_file_system_snapshot_object=snapshot_part,
            )
