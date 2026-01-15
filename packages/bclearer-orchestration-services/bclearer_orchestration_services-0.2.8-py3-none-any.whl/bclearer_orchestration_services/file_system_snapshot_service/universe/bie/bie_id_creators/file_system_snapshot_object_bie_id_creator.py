from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.snapshot_domains import (
    SnapshotDomains,
)


def create_file_system_snapshot_object_bie_id(
    base_system_object_bie_id: BieIds,
    owning_snapshot_domain: SnapshotDomains,
) -> BieIds:
    input_objects = [
        BieFileSystemSnapshotDomainTypes.BIE_FILE_SYSTEM_SNAPSHOT_BASE_SNAPSHOT_BIE_IDS.item_bie_identity,
        owning_snapshot_domain.bie_id,
        base_system_object_bie_id,
    ]

    file_system_snapshot_object_base_snapshot_object_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    return file_system_snapshot_object_base_snapshot_object_bie_id
