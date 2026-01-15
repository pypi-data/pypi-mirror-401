from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.bie_id_to_sum_adder import (
    add_bie_id_to_sum,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.sum_objects import (
    SumObjects,
)


def add_bie_id_to_sum_dictionary(
    sum_objects_dictionary,
    bie_id,
    bie_id_type,
    direction: BieFileSystemSnapshotDomainTypes,
) -> None:
    if (
        bie_id_type
        in sum_objects_dictionary
    ):
        sum_object = add_bie_id_to_sum(
            sum_object=sum_objects_dictionary[
                bie_id_type
            ],
            bie_id=bie_id,
        )

    else:
        sum_object = SumObjects(
            bie_id=bie_id,
            direction_type=direction,
            bie_summed_type=bie_id_type,
        )

    sum_objects_dictionary[
        bie_id_type
    ] = sum_object
