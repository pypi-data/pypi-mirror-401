from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.common_knowledge.snapshot_domain_literals import (
    SnapshotDomainLiterals,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.algorithmic_contents import (
    AlgorithmicContents,
)


class FileByteContents(
    AlgorithmicContents
):
    def __init__(self, bie_id: BieIds):
        super().__init__(
            bie_id=bie_id,
            base_hr_name=SnapshotDomainLiterals.file_byte_content,
            bie_domain_type=BieFileSystemSnapshotDomainTypes.BIE_FILE_BYTE_CONTENTS,
        )
