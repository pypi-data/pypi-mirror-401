from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.root_relative_paths import (
    RootRelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
    FileSystemSnapshotObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.exclusive_ancestor_snapshot_sum_objects_populator import (
    populate_exclusive_ancestor_snapshot_sum_objects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.exclusive_descendant_snapshot_sum_objects_populator import (
    populate_exclusive_descendant_snapshot_sum_objects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.inclusive_ancestor_snapshot_sum_objects_populator import (
    populate_inclusive_ancestor_snapshot_sum_objects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.inclusive_descendant_snapshot_sum_objects_populator import (
    populate_inclusive_descendant_snapshot_sum_objects,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def populate_snapshot_sum_objects(
    root_relative_path: RootRelativePaths,
) -> None:
    if isinstance(
        root_relative_path.snapshot,
        FileSystemSnapshotObjects,
    ):
        populate_inclusive_ancestor_snapshot_sum_objects(
            file_system_snapshot_object=root_relative_path.snapshot
        )

        populate_inclusive_descendant_snapshot_sum_objects(
            file_system_snapshot_object=root_relative_path.snapshot
        )

        populate_exclusive_ancestor_snapshot_sum_objects(
            file_system_snapshot_object=root_relative_path.snapshot
        )

        populate_exclusive_descendant_snapshot_sum_objects(
            file_system_snapshot_object=root_relative_path.snapshot
        )
