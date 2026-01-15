from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
    FileSystemSnapshotObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.bie_id_to_sum_dictionary_by_type_adder import (
    add_bie_id_to_sum_dictionary_by_type,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def populate_exclusive_descendant_snapshot_sum_objects(
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    __accumulate_descendants(
        file_system_snapshot_object=file_system_snapshot_object
    )


def __accumulate_descendants(
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    for (
        child
    ) in (
        file_system_snapshot_object.parts
    ):
        __accumulate_descendants(child)

    for (
        child
    ) in (
        file_system_snapshot_object.parts
    ):
        add_bie_id_to_sum_dictionary_by_type(
            source_bie_objects_dictionary=child.exclusive_descendant_sum_objects,
            target_sum_objects_dictionary=file_system_snapshot_object.exclusive_descendant_sum_objects,
            direction=BieFileSystemSnapshotDomainTypes.DESCENDENTS,
        )

        add_bie_id_to_sum_dictionary_by_type(
            source_bie_objects_dictionary=child.extended_objects,
            target_sum_objects_dictionary=file_system_snapshot_object.exclusive_descendant_sum_objects,
            direction=BieFileSystemSnapshotDomainTypes.DESCENDENTS,
        )
