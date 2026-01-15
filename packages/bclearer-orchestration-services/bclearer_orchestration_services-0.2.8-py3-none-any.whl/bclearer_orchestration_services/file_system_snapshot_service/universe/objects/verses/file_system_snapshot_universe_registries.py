from bclearer_core.infrastructure.nf.objects.registries.nf_domain_universe_registries import (
    NfDomainUniverseRegistries,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_id_creators.maximal_snapshot_domain_bie_id_creator import (
    create_maximal_snapshot_domain_bie_id,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.exporters.tables.fssu_registries_dataframes_dictionary_creator import (
    create_fssu_registries_dataframes_dictionary,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.profiles.file_system_snapshot_container_bie_id_profiles import (
    FileSystemSnapshotContainerBieIdProfiles,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.getters.individual_file_system_snapshot_files_from_file_system_snapshots_getter import (
    get_individual_file_system_snapshot_files_from_file_system_snapshots,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.getters.universe_individual_file_system_snapshot_objects_populator import (
    populate_universe_individual_file_system_snapshot_objects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.bie_signatures.root_relative_path_bie_signatures_populator import (
    populate_root_relative_path_bie_signatures,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.file_system_snapshot_objects.root_relative_path_populator import (
    populate_root_relative_path,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.root_relative_path_creator import (
    create_root_relative_path,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.sum_objects.snapshot_sum_objects_populator import (
    populate_snapshot_sum_objects,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.maximal_snapshot_domains import (
    MaximalSnapshotDomains,
)


class FileSystemSnapshotUniverseRegistries(
    NfDomainUniverseRegistries
):
    def __init__(
        self,
        owning_file_system_snapshot_universe,
        root_file_system_object: FileSystemObjects,
    ) -> None:
        super().__init__()

        from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
            FileSystemSnapshotUniverses,
        )

        if not isinstance(
            owning_file_system_snapshot_universe,
            FileSystemSnapshotUniverses,
        ):
            raise TypeError

        self.owning_universe = owning_file_system_snapshot_universe

        maximal_snapshot_domain_bie_id = create_maximal_snapshot_domain_bie_id(
            app_run_session_object=self.owning_universe.app_run_session_object
        )

        self.maximal_snapshot_domain = MaximalSnapshotDomains(
            bie_id=maximal_snapshot_domain_bie_id,
            base_hr_name="maximal_snapshot_domain",
            bie_domain_type=BieFileSystemSnapshotDomainTypes.MAXIMAL_SNAPSHOT_DOMAINS,
        )

        self.root_relative_path = create_root_relative_path(
            file_system_object=root_file_system_object,
            owning_snapshot_domain=self.maximal_snapshot_domain,
        )

        populate_root_relative_path(
            root_relative_path=self.root_relative_path
        )

        populate_snapshot_sum_objects(
            root_relative_path=self.root_relative_path
        )

        self.file_system_snapshot_container_bie_id_profile = FileSystemSnapshotContainerBieIdProfiles(
            root_relative_path=self.root_relative_path
        )

        populate_root_relative_path_bie_signatures(
            bie_signature_registry=self.file_system_snapshot_container_bie_id_profile.root_bie_signature_registry,
            root_relative_path=self.root_relative_path,
        )

        self.file_system_snapshot_container_bie_id_profile.populate_signature_comparisons()

    def export_register_as_dictionary(
        self,
    ) -> dict:
        # TODO: to be replaced
        export_register_as_dictionary = create_fssu_registries_dataframes_dictionary(
            file_system_snapshot_universe_registry=self
        )

        return export_register_as_dictionary

    def get_individual_file_system_snapshot_objects(
        self,
    ) -> list:
        universe_individual_file_system_snapshot_objects = (
            list()
        )

        populate_universe_individual_file_system_snapshot_objects(
            file_system_snapshot_universe_registry=self,
            universe_individual_file_system_snapshot_objects=universe_individual_file_system_snapshot_objects,
        )

        return universe_individual_file_system_snapshot_objects

    # TODO: do the sister method for Folders?? Later
    def get_only_individual_file_system_snapshot_files(
        self,
    ) -> list:
        universe_individual_file_system_snapshot_objects = (
            self.get_individual_file_system_snapshot_objects()
        )

        universe_individual_file_system_snapshot_files = get_individual_file_system_snapshot_files_from_file_system_snapshots(
            file_system_snapshots=universe_individual_file_system_snapshot_objects
        )

        return universe_individual_file_system_snapshot_files
