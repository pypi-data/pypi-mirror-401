from pathlib import Path

from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.relative_paths import (
    RelativePaths,
)


class NonRootRelativePaths(
    RelativePaths
):
    def __init__(
        self,
        relative_path: Path,
        relative_path_parent: "RelativePaths",
    ):
        self.relative_path_parent = (
            relative_path_parent
        )

        super().__init__(
            base_hr_name=relative_path.name,
            relative_path=relative_path,
        )

        relative_path_parent.add_relative_path_child(
            relative_path_child=self
        )
