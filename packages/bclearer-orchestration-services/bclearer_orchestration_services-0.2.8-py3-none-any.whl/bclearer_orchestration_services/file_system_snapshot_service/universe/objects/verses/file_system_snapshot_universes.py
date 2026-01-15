from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
    HR_NAME_COMPONENT_DIVIDER,
)
from bclearer_core.infrastructure.nf.objects.verses.nf_domain_universes import (
    NfDomainUniverses,
)
from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_file_system_snapshot_universes import (
    BieFileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_ids_registerers.fssu_domain_bie_ids_registerer import (
    register_fssu_domain_bie_ids,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_app_run_session_types import (
    FileSystemSnapshotAppRunSessionTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_universe_types import (
    FileSystemSnapshotUniverseTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.exporters.file_system_snapshot_universe_if_inspection_is_enabled_exporter import (
    export_file_system_snapshot_universe_if_inspection_is_enabled,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.profiles.file_system_snapshot_container_bie_id_profiles import (
    FileSystemSnapshotContainerBieIdProfiles,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_container_bie_id_profile_wrappers import (
    FileSystemSnapshotContainerBieIdProfileWrappers,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class FileSystemSnapshotUniverses(
    NfDomainUniverses
):
    def __init__(
        self,
        parallel_bie_universe: BieFileSystemSnapshotUniverses,
        root_file_system_object: FileSystemObjects,
    ) -> None:
        super().__init__()

        self.app_run_session_object = AppRunSessionObjects(
            bie_app_run_session_type=FileSystemSnapshotAppRunSessionTypes.FILE_SYSTEM_SNAPSHOT_APP_RUN_SESSION
        )

        self.file_system_snapshot_universe_registry = FileSystemSnapshotUniverseRegistries(
            owning_file_system_snapshot_universe=self,
            root_file_system_object=root_file_system_object,
        )

        self.bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                FileSystemSnapshotUniverseTypes.FILE_SYSTEM_SNAPSHOT_UNIVERSE.item_bie_identity,
                self.app_run_session_object.bie_id,
            ]
        )

        self.base_hr_name = (
            FileSystemSnapshotUniverseTypes.FILE_SYSTEM_SNAPSHOT_UNIVERSE.b_enum_item_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.app_run_session_object.app_run_session_date_time.strftime(
                format=HR_DATE_TIME_FORMAT
            )
        )

        # TODO: unused code for FSSO tests (use cases and export) - to be implemented
        self.parallel_bie_universe = (
            parallel_bie_universe
        )

        register_fssu_domain_bie_ids(
            bie_universe=parallel_bie_universe,
            file_system_snapshot_universe_registry=self.file_system_snapshot_universe_registry,
        )

    def inspect_me(
        self,
        service_workspace_configuration: WorkspaceConfigurations,
    ) -> None:
        export_file_system_snapshot_universe_if_inspection_is_enabled(
            file_system_snapshot_universe=self,
            service_workspace_configuration=service_workspace_configuration,
        )

    # TODO 2025109 pytest-fss OXi - need to design
    def get_my_bie_id_profile(
        self,
    ) -> FileSystemSnapshotContainerBieIdProfiles:
        file_system_snapshot_universe_bie_profile = (
            self.file_system_snapshot_universe_registry.file_system_snapshot_container_bie_id_profile
        )

        return file_system_snapshot_universe_bie_profile
