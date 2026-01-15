import pathlib

from bclearer_core.configurations.b_configurations.b_configurations import (
    BConfigurations,
)
from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_domain_literals import (
    FileSystemSnapshotDomainLiterals,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.exporters.fssu_registry_to_access_database_exporter import (
    export_fssu_registry_to_access_database,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.exporters.fssu_registry_to_sqlite_database_exporter import (
    export_fssu_registry_to_sqlite_database,
)
from bclearer_orchestration_services.operating_system_services.is_platform_windows_checker import (
    check_is_platform_windows,
)


# TODO: add checks for: ADD_GRAPHML_INSPECTION and ENABLE_GRAPH_INSPECTIONS. Split by level: add new functions for Database and Graph.
#   Add an empty function for graph_ml_inspection
# TODO: Move out of the test/ folder, otherwise it will cause problems when imported from other repository
def export_file_system_snapshot_universe_if_inspection_is_enabled(
    file_system_snapshot_universe: "FileSystemSnapshotUniverses",
    service_workspace_configuration: WorkspaceConfigurations,
) -> None:
    # TODO: check that what called this is the FSSUniverse - look in the python utility for example of implementation
    # TODO: this variable has to be created and added a by-default value to TRUE - DONE
    from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universes import (
        FileSystemSnapshotUniverses,
    )

    if not isinstance(
        file_system_snapshot_universe,
        FileSystemSnapshotUniverses,
    ):
        message = (
            export_file_system_snapshot_universe_if_inspection_is_enabled.__name__
        )

        raise TypeError(message)

    if (
        not BConfigurations.ENABLE_DATABASE_INSPECTION
    ):
        return

    test_case_output_folder = service_workspace_configuration.this_run_workspace.get_descendant_file_system_folder(
        relative_path=pathlib.Path(
            FileSystemSnapshotDomainLiterals.snapshot_universe_domain_name
        )
    )

    test_case_output_folder.make_me_on_disk()

    dataframes_dictionary_keyed_on_string = (
        file_system_snapshot_universe.file_system_snapshot_universe_registry.export_register_as_dictionary()
    )

    fssu_registry_database_base_name = __get_fssu_registry_database_base_name(
        service_workspace_configuration=service_workspace_configuration
    )

    enable_access_inspection = (
        BConfigurations.ENABLE_MS_ACCESS_DATABASE_INSPECTION
        and check_is_platform_windows()
    )

    if enable_access_inspection:
        export_fssu_registry_to_access_database(
            dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
            test_case_output_folder=test_case_output_folder,
            fssu_registry_database_base_name=fssu_registry_database_base_name,
        )

    if (
        BConfigurations.ENABLE_SQLITE_DATABASE_INSPECTION
    ):
        export_fssu_registry_to_sqlite_database(
            dataframes_dictionary_keyed_on_string=dataframes_dictionary_keyed_on_string,
            test_case_output_folder=test_case_output_folder,
            fssu_registry_database_base_name=fssu_registry_database_base_name,
        )


def __get_fssu_registry_database_base_name(
    service_workspace_configuration: WorkspaceConfigurations,
) -> str:
    database_base_name_components = [
        component
        for component in (
            FileSystemSnapshotDomainLiterals.snapshot_universe_domain_name,
            service_workspace_configuration.this_run_human_readable_short_name,
        )
        if component
    ]

    database_base_name = "_".join(
        database_base_name_components
    )

    return database_base_name
