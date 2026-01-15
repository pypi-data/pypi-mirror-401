from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
    FileSystemSnapshotUniverses,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.orchestrators.file_system_snapshot_universe_getter import (
    get_file_system_snapshot_universe,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.reporters.signature_vs_sum_discordances_reporter import (
    report_signature_vs_sum_discordances,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


# TODO: Find all calls and move here
@run_and_log_function
def handle_file_system_snapshot_service(
    file_system_snapshot_configuration: FileSystemSnapshotConfigurations,
) -> FileSystemSnapshotUniverses:
    # TODO: Create app session object and pass it in?
    file_system_snapshot_universe = get_file_system_snapshot_universe(
        file_system_snapshot_configuration=file_system_snapshot_configuration
    )

    report_signature_vs_sum_discordances(
        file_system_snapshot_universe=file_system_snapshot_universe
    )

    return file_system_snapshot_universe
