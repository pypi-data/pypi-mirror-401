from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.bie_id_to_sum_dictionary_adder import (
    add_bie_id_to_sum_dictionary,
)


def add_bie_id_to_sum_dictionary_by_type(
    source_bie_objects_dictionary: dict,
    target_sum_objects_dictionary: dict,
    direction: BieFileSystemSnapshotDomainTypes,
) -> None:
    for (
        bie_id_type,
        bie_object,
    ) in (
        source_bie_objects_dictionary.items()
    ):
        add_bie_id_to_sum_dictionary(
            sum_objects_dictionary=target_sum_objects_dictionary,
            bie_id=bie_object.bie_id,
            bie_id_type=bie_id_type,
            direction=direction,
        )
