from bclearer_core.infrastructure.session.operating_system.bie_operating_system_types import (
    BieOperatingSystemTypes,
)
from bclearer_core.infrastructure.session.os_user_session.bie_os_user_profile_session_types import (
    BieOsUserProfileSessionTypes,
)
from bclearer_core.infrastructure.session.user.bie_os_user_profile_types import (
    BieOsUserProfileTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.common_knowledge.bie_file_system_snapshot_multiverse_types import (
    FileSystemSnapshotMultiverseTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_file_system_snapshot_universes import (
    BieFileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_app_run_session_types import (
    FileSystemSnapshotAppRunSessionTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_universe_types import (
    FileSystemSnapshotUniverseTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.orchestrators.bie_infrastructure_orchestrator import (
    orchestrate_bie_infrastructure,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


# TODO: to be deprecated?? follow usages to double check
@run_and_log_function
def get_bie_file_system_snapshot_object_universe() -> (
    BieFileSystemSnapshotUniverses
):
    reportable_additional_enums = [
        BieFileSystemSnapshotDomainTypes,
        FileSystemSnapshotAppRunSessionTypes,
        BieOsUserProfileSessionTypes,
        BieOperatingSystemTypes,
        FileSystemSnapshotUniverseTypes,
        FileSystemSnapshotMultiverseTypes,
        BieOsUserProfileTypes,
    ]

    bie_file_system_object_universe = orchestrate_bie_infrastructure(
        reportable_additional_enums=reportable_additional_enums,
        bie_universe_type=BieFileSystemSnapshotUniverses,
    )

    # register_bie_model_nodes(
    #     bie_registry=parallel_bie_universe.bie_infrastructure_registry)

    if not isinstance(
        bie_file_system_object_universe,
        BieFileSystemSnapshotUniverses,
    ):
        raise TypeError

    return (
        bie_file_system_object_universe
    )
