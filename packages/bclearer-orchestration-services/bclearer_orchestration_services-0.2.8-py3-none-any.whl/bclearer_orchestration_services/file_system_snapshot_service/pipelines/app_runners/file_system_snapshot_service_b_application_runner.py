"""File System Snapshot Service B Application Runner

This module provides the runner for executing the file system snapshot service b_application.
"""

from bclearer_orchestration_services.file_system_snapshot_service.pipelines.app_runners.file_system_snapshot_service_b_application import (
    file_system_snapshot_service_b_application,
)


def run_b_application_file_system_snapshot_service() -> (
    None
):
    """
    Run the file system snapshot service as a b_application.

    This is the main entry point for running file system snapshots in the b_application framework.
    It delegates to the b_application function which handles the complete workflow.
    """
    file_system_snapshot_service_b_application()
