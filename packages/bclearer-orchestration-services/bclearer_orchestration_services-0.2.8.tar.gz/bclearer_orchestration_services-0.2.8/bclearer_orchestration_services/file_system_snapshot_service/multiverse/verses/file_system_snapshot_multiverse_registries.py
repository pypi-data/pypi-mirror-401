from typing import Dict

from bclearer_core.infrastructure.nf.objects.registries.nf_multiverse_registries import (
    NfMultiverseRegistries,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class FileSystemSnapshotMultiverseRegistries(
    NfMultiverseRegistries
):
    def __init__(
        self,
        owning_file_system_snapshot_multiverse,
    ) -> None:
        super().__init__()

        from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
            FileSystemSnapshotMultiverses,
        )

        if not isinstance(
            owning_file_system_snapshot_multiverse,
            FileSystemSnapshotMultiverses,
        ):
            raise TypeError

        self.owning_multiverse = owning_file_system_snapshot_multiverse

        # TODO: Should register be of type ...Registers?
        self.file_system_snapshot_universes_register: Dict[
            BieIds,
            FileSystemSnapshotUniverses,
        ] = dict()

    # TODO: to be deprecated??
    def add_file_system_snapshot_universes_as_dictionary_to_registry(
        self,
        file_system_snapshot_universes_dictionary,
    ) -> None:
        self.file_system_snapshot_universes_register = file_system_snapshot_universes_dictionary

    def add_universe(
        self,
        file_system_snapshot_universe: FileSystemSnapshotUniverses,
    ) -> None:
        self.file_system_snapshot_universes_register[
            file_system_snapshot_universe.bie_id
        ] = file_system_snapshot_universe

    # TODO: added here as a placeholder for the HR queries - stage 2
    @staticmethod
    def export_multiverse_register_as_dictionary() -> (
        dict
    ):
        # TODO: to complete
        file_system_snapshot_multiverse_register_as_dictionary = (
            dict()
        )

        return file_system_snapshot_multiverse_register_as_dictionary
