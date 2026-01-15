from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.maximal_snapshot_domains import (
    MaximalSnapshotDomains,
)


def register_maximal_snapshot_domain(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    maximal_snapshot_domain: MaximalSnapshotDomains,
    snapshot_universe,
) -> None:
    bie_infrastructure_registry.register_bie_object_and_type_instance(
        bie_object=maximal_snapshot_domain
    )

    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=maximal_snapshot_domain.bie_id,
        bie_place_2_id=snapshot_universe.bie_id,
        bie_relation_type_id=BieCoreRelationTypes.BIE_COUPLES.item_bie_identity,
    )
