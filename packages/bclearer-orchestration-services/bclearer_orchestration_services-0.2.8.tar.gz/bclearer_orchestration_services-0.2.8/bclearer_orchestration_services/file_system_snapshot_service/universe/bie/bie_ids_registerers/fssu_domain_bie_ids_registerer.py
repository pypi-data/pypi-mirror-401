from bclearer_core.infrastructure.session.bie_id_registerers.infrastructure_bie_ids_registerer import (
    register_infrastructure_bie_ids,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_file_system_snapshot_universes import (
    BieFileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_ids_registerers.file_system_snapshot_universe_bie_ids_registerer import (
    register_file_system_snapshot_universe_bie_ids,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_ids_registerers.maximal_snapshot_domain_registerer import (
    register_maximal_snapshot_domain,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_ids_registerers.snapshot_bie_ids_registerer import (
    register_snapshot_bie_ids,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)


def register_fssu_domain_bie_ids(
    bie_universe: BieFileSystemSnapshotUniverses,
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> None:
    bie_infrastructure_registry = (
        bie_universe.bie_infrastructure_registry
    )

    register_infrastructure_bie_ids(
        bie_infrastructure_registry=bie_infrastructure_registry,
        app_run_session_object=file_system_snapshot_universe_registry.owning_universe.app_run_session_object,
    )

    register_maximal_snapshot_domain(
        bie_infrastructure_registry=bie_infrastructure_registry,
        maximal_snapshot_domain=file_system_snapshot_universe_registry.maximal_snapshot_domain,
        snapshot_universe=file_system_snapshot_universe_registry.owning_universe,
    )

    register_file_system_snapshot_universe_bie_ids(
        bie_infrastructure_registry=bie_infrastructure_registry,
        file_system_snapshot_universe_registry=file_system_snapshot_universe_registry,
    )

    register_snapshot_bie_ids(
        bie_infrastructure_registry=bie_infrastructure_registry,
        file_system_snapshot_universe_registry=file_system_snapshot_universe_registry,
    )
