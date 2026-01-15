from pathlib import Path

from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_domain_literals import (
    FileSystemSnapshotDomainLiterals,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.relative_paths import (
    RelativePaths,
)


class RootRelativePaths(RelativePaths):
    def __init__(self):
        relative_path = Path(str())

        super().__init__(
            base_hr_name=FileSystemSnapshotDomainLiterals.root_relative_path,
            relative_path=relative_path,
        )
