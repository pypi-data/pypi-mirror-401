from bclearer_core.constants.standard_constants import (
    HR_DATE_TIME_FORMAT,
    HR_NAME_COMPONENT_DIVIDER,
)
from bclearer_core.infrastructure.nf.objects.verses.nf_multiverses import (
    NfMultiverses,
)
from bclearer_core.infrastructure.session.app_run_session.app_run_session_objects import (
    AppRunSessionObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.common_knowledge.bie_file_system_snapshot_multiverse_types import (
    FileSystemSnapshotMultiverseTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverse_registries import (
    FileSystemSnapshotMultiverseRegistries,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_app_run_session_types import (
    FileSystemSnapshotAppRunSessionTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)


class FileSystemSnapshotMultiverses(
    NfMultiverses
):
    def __init__(self):
        super().__init__()

        self.file_system_snapshot_multiverse_registry = FileSystemSnapshotMultiverseRegistries(
            owning_file_system_snapshot_multiverse=self
        )

        self.app_run_session_object = AppRunSessionObjects(
            bie_app_run_session_type=FileSystemSnapshotAppRunSessionTypes.FILE_SYSTEM_SNAPSHOT_APP_RUN_SESSION
        )

        self.bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                FileSystemSnapshotMultiverseTypes.FILE_SYSTEM_SNAPSHOT_MULTIVERSE.item_bie_identity,
                self.app_run_session_object.bie_id,
            ]
        )

        self.base_hr_name = (
            FileSystemSnapshotMultiverseTypes.FILE_SYSTEM_SNAPSHOT_MULTIVERSE.b_enum_item_name
            + HR_NAME_COMPONENT_DIVIDER
            + self.app_run_session_object.app_run_session_date_time.strftime(
                format=HR_DATE_TIME_FORMAT
            )
        )

    def add_universe_to_registry(
        self,
        file_system_snapshot_universe: FileSystemSnapshotUniverses,
    ) -> None:
        self.file_system_snapshot_multiverse_registry.add_universe(
            file_system_snapshot_universe=file_system_snapshot_universe
        )

    def is_universes_register_empty(
        self,
    ) -> bool:
        multiverse_universes_register = (
            self.file_system_snapshot_multiverse_registry.file_system_snapshot_universes_register
        )

        if (
            not multiverse_universes_register
        ):
            return True

        return False
