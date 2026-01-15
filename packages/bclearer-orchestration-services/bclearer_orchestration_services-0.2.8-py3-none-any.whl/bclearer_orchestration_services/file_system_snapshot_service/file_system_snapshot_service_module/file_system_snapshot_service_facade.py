from bclearer_orchestration_services.file_system_snapshot_service.multiverse.configurations.file_system_snapshots_configurations import (
    FileSystemSnapshotsConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.orchestrators.file_system_snapshots_multiverse_analyse_orchestrator import (
    orchestrate_file_system_snapshots_multiverse_analyse,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.orchestrators.file_system_snapshots_multiverse_run_and_export_orchestrator import (
    orchestrate_file_system_snapshots_multiverse_run_and_export,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.orchestrators.file_system_snapshots_multiverse_run_export_and_analyse_orchestrator import (
    orchestrate_file_system_snapshots_multiverse_run_export_and_analyse,
)
from bclearer_orchestration_services.file_system_snapshot_service.multiverse.verses.file_system_snapshot_multiverses import (
    FileSystemSnapshotMultiverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.orchestrators.file_system_snapshot_universe_getter import (
    get_file_system_snapshot_universe,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.orchestrators.file_system_snapshot_universe_run_and_export_orchestrator import (
    orchestrate_file_system_snapshot_universe_run_and_export,
)


class FileSystemSnapshotServiceFacade:
    @staticmethod
    def run_file_system_snapshot(
        file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
    ) -> FileSystemSnapshotUniverses:
        return get_file_system_snapshot_universe(
            file_system_snapshot_configuration=file_system_snapshot_configuration
        )

    @staticmethod
    def run_and_export_file_system_snapshot(
        file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
    ) -> FileSystemSnapshotUniverses:
        return orchestrate_file_system_snapshot_universe_run_and_export(
            file_system_snapshot_configuration=file_system_snapshot_configuration
        )

    @staticmethod
    def run_and_export_file_system_snapshots(
        file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
    ) -> FileSystemSnapshotMultiverses:
        return orchestrate_file_system_snapshots_multiverse_run_and_export(
            file_system_snapshots_configuration=file_system_snapshots_configuration
        )

    @staticmethod
    def analyse_file_system_snapshots(
        file_system_snapshot_multiverse: FileSystemSnapshotMultiverses,
    ):
        orchestrate_file_system_snapshots_multiverse_analyse(
            file_system_snapshot_multiverse=file_system_snapshot_multiverse
        )

    @staticmethod
    def run_export_and_analyse_file_system_snapshots(
        file_system_snapshots_configuration: FileSystemSnapshotsConfigurations,
    ):
        return orchestrate_file_system_snapshots_multiverse_run_export_and_analyse(
            file_system_snapshots_configuration=file_system_snapshots_configuration
        )
