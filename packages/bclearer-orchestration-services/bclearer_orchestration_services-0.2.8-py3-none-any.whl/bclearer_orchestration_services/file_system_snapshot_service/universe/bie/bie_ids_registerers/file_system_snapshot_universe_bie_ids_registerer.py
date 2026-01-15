from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_universe_types import (
    FileSystemSnapshotUniverseTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import (
    BSequenceNames,
)


def register_file_system_snapshot_universe_bie_ids(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> None:
    file_system_snapshot_universe = (
        file_system_snapshot_universe_registry.owning_universe
    )

    bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            file_system_snapshot_universe.base_hr_name
        ]
    )

    bie_infrastructure_registry.register_bie_id_and_type_instance(
        bie_item_id=file_system_snapshot_universe.bie_id,
        bie_sequence_name=bie_sequence_name,
        bie_id_type_id=FileSystemSnapshotUniverseTypes.FILE_SYSTEM_SNAPSHOT_UNIVERSE.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=file_system_snapshot_universe.bie_id,
        bie_place_2_id=file_system_snapshot_universe.app_run_session_object.bie_id,
        bie_relation_type_id=BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity,
    )
