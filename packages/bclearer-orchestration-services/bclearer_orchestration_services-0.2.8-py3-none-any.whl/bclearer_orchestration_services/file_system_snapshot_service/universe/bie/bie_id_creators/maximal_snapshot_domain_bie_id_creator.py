from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_maximal_snapshot_domain_bie_id(
    app_run_session_object: AppRunSessionObjects,
) -> BieIds:
    input_objects = [
        BieFileSystemSnapshotDomainTypes.MAXIMAL_SNAPSHOT_DOMAINS.item_bie_identity,
        app_run_session_object.bie_id,
    ]

    maximal_snapshot_domain_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    return (
        maximal_snapshot_domain_bie_id
    )
