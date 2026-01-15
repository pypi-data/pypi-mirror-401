"""File System Snapshot Service Single Input UI Startup

This module provides the UI startup configuration for single input folder snapshots.
"""

from bclearer_orchestration_services.file_system_snapshot_service.pipelines.app_runners.file_system_snapshot_service_b_application_runner import (
    run_b_application_file_system_snapshot_service,
)


def configure_and_run_single_input_snapshot() -> (
    None
):
    """
    Configure and run a file system snapshot with a single input folder.

    This function:
    1. Sets up workspace configuration for single input mode
    2. Runs the snapshot b_application
    """
    # TODO: Add workspace configuration setup similar to nf_common_utilities pattern
    # For now, this is a simplified version that directly calls the runner
    run_b_application_file_system_snapshot_service()


if __name__ == "__main__":
    configure_and_run_single_input_snapshot()
