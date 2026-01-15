"""File System Snapshot Service B Application

This module provides the b_application wrapper for the file system snapshot service.
It serves as the entry point for running file system snapshots through the b_application framework.
"""

from bclearer_orchestration_services.file_system_snapshot_service.file_system_snapshot_service_module.file_system_snapshot_service_facade import (
    FileSystemSnapshotServiceFacade,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.file_system_snapshot_configurations import (
    FileSystemSnapshotConfigurations,
)


def file_system_snapshot_service_b_application() -> (
    None
):
    """
    B Application entry point for file system snapshot service.

    This function orchestrates a complete file system snapshot workflow:
    1. Reads configuration from FileSystemSnapshotConfigurations
    2. Runs the snapshot
    3. Exports the results
    """
    file_system_snapshot_configuration = (
        FileSystemSnapshotConfigurations()
    )

    FileSystemSnapshotServiceFacade.run_and_export_file_system_snapshot(
        file_system_snapshot_configuration=file_system_snapshot_configuration
    )
