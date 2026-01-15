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
def populate_inclusive_ancestor_snapshot_sum_objects(
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    __add_parent_to_children(
        file_system_snapshot_object=file_system_snapshot_object
    )


def __add_parent_to_children(
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    add_bie_id_to_sum_dictionary_by_type(
        source_bie_objects_dictionary=file_system_snapshot_object.extended_objects,
        target_sum_objects_dictionary=file_system_snapshot_object.inclusive_ancestor_sum_objects,
        direction=BieFileSystemSnapshotDomainTypes.ANCESTORS,
    )

    for (
        part
    ) in (
        file_system_snapshot_object.parts
    ):
        __add_parent_to_child(
            parent_file_system_snapshot_object=file_system_snapshot_object,
            child_file_system_snapshot_object=part,
        )

        __add_parent_to_children(
            file_system_snapshot_object=part
        )


def __add_parent_to_child(
    parent_file_system_snapshot_object: FileSystemSnapshotObjects,
    child_file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    add_bie_id_to_sum_dictionary_by_type(
        source_bie_objects_dictionary=parent_file_system_snapshot_object.inclusive_ancestor_sum_objects,
        target_sum_objects_dictionary=child_file_system_snapshot_object.inclusive_ancestor_sum_objects,
        direction=BieFileSystemSnapshotDomainTypes.ANCESTORS,
    )
